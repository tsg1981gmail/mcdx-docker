"""整理引擎：源目录刮削 → 按命名模板在目标库生成 硬链接（同盘）或复制（跨盘）。

设计（来自整理可行性分析）：
- 复用 mdcx 各环节：get_file_info_v2（解析番号）→ FileScraper.run（刮削）
  → get_output_name（命名模板渲染目标路径）→ write_nfo（写元数据）。
- 新写 link_or_copy：os.link → EXDEV/EROFS/EPERM 等失败自动回退 shutil.copy2 原子复制。
- 源文件保持不动（保种）；目标已存在且同源（硬链接/inode 相同）视为完成跳过。
- 可选：按首个海报 URL 直拉封面（不依赖 Qt OtherInfo 链）。
"""
from __future__ import annotations

import asyncio
import logging
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

log = logging.getLogger("mdcx.web")

ProgressCb = Callable[[int, int], None]  # (done, total)

VIDEO_EXT = (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".ts", ".m2ts",
             ".rmvb", ".rm", ".webm", ".mpg", ".mpeg", ".3gp", ".vob")


@dataclass
class OrganizeItem:
    src: str
    target: str
    action: str        # linked | copied | skipped | failed | no_meta
    detail: str = ""
    nfo: str = ""


async def _link_or_copy(src: Path, dst: Path, prefer: str) -> tuple[bool, str]:
    """硬链接/软链接/复制；目标已存在且同源→跳过；链接失败自动回退复制。返回 (ok, 说明)。"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        try:
            if os.path.samefile(src, dst):
                return True, "目标已存在且同源，跳过"
        except OSError:
            pass
        return False, "目标已存在（不同文件），跳过"
    if prefer == "hardlink":
        try:
            os.link(src, dst)
            return True, "硬链接"
        except OSError as exc:
            (code, _) = (getattr(exc, "errno", None), exc)
            if code not in (18, 30, 1):  # EXDEV, EROFS, EPERM 之外仍报告失败
                return False, f"硬链接失败: {exc}"
            log.info("hardlink cross-device/ro for %s -> %s, fallback copy", src, dst)
    elif prefer == "symlink":
        try:
            os.symlink(src.resolve(), dst)
            return True, "软链接"
        except OSError as exc:
            log.info("symlink failed for %s -> %s: %s, fallback copy", src, dst, exc)
    try:
        await asyncio.to_thread(_copy_atomic, src, dst)
        return True, "复制" if prefer != "hardlink" else "复制(硬链接不可用回退)"
    except OSError as exc:
        return False, f"复制失败: {exc}"


def _copy_atomic(src: Path, dst: Path) -> None:
    tmp = dst.with_name(dst.name + ".mdcx-tmp")
    shutil.copy2(src, tmp)
    os.replace(tmp, dst)


class Organizer:
    def __init__(self, library_root: Path, mode: str = "hardlink",
                 on_progress: ProgressCb | None = None, on_log: Callable[[str], None] | None = None,
                 download_poster: bool = True) -> None:
        self.library_root = library_root.resolve()
        self.mode = mode if mode in ("hardlink", "copy", "symlink") else "hardlink"
        self.on_progress = on_progress
        self.on_log = on_log
        self.download_poster = download_poster

    def _info(self, msg: str) -> None:
        log.info("%s", msg)
        if self.on_log:
            self.on_log(msg)

    async def organize_paths(self, files: list[Path], concurrency: int = 4,
                             stop: asyncio.Event | None = None) -> list[OrganizeItem]:
        from mdcx.config.manager import manager
        from mdcx.crawler import CrawlerProvider
        from mdcx.core.file import get_file_info_v2, get_output_name
        from mdcx.core.file_crawler import FileScraper
        from mdcx.core.nfo import write_nfo
        from mdcx.models.enums import FileMode

        results: list[OrganizeItem] = []
        self.library_root.mkdir(parents=True, exist_ok=True)
        sem = asyncio.Semaphore(concurrency)

        async with manager.acquire_computed() as computed:
            provider = CrawlerProvider(manager.config, computed.async_client,
                                       config_getter=lambda: manager.config)
            fs = FileScraper(manager.config, provider)
            done = 0

            def bump(item: OrganizeItem) -> None:
                results.append(item)
                nonlocal done
                done += 1
                if self.on_progress:
                    self.on_progress(done, len(files))

            async def one(file: Path) -> None:
                if stop is not None and stop.is_set():
                    bump(OrganizeItem(str(file), "", "skipped", "已取消"))
                    return
                file = file.resolve()
                try:
                    fi = await get_file_info_v2(file)
                    res = await fs.run(fi.crawl_task(), FileMode.Default)
                    if res is None or getattr(res, "number", "") is None:
                        bump(OrganizeItem(str(file), "", "no_meta", "刮削未返回结果（可能无匹配或站点不可达）"))
                        return
                    file_ex = fi.file_ex if fi.file_ex else file.suffix.lower()
                    (folder_new, file_new, nfo_new, _pnt, _tnt, _fnt, _rule,
                     poster_final, _thumb_final, _fanart_final) = get_output_name(
                        fi, res, self.library_root, file_ex)
                    ok, msg = await _link_or_copy(file, file_new, self.mode)
                    nfo_path = ""
                    try:
                        # update=True 才会真正写盘（update=False 是"不写"守护分支）
                        await write_nfo(fi, res, nfo_new, folder_new, update=True)
                        nfo_path = str(nfo_new)
                        self._info(f"nfo 写入: {nfo_new}")
                    except Exception as exc:  # noqa: BLE001
                        self._info(f"nfo 写入失败: {exc}")
                    if self.download_poster:
                        try:
                            await self._fetch_poster(computed, res, poster_final)
                        except Exception as exc:  # noqa: BLE001
                            self._info(f"海报下载失败: {exc}")
                    action = "linked" if "链接" in msg else ("copied" if "复制" in msg else "skipped")
                    bump(OrganizeItem(str(file), str(file_new), action, msg, nfo_path))
                except asyncio.CancelledError:
                    bump(OrganizeItem(str(file), "", "skipped", "已取消"))
                except Exception as exc:  # noqa: BLE001
                    log.exception("organize %s failed", file)
                    bump(OrganizeItem(str(file), "", "failed", str(exc)))
                    if self.on_log:
                        self.on_log(f"失败 {file}: {exc}")

            tasks = [asyncio.create_task(one(f)) for f in files]
            await asyncio.gather(*tasks, return_exceptions=True)

        return results

    async def _fetch_poster(self, computed, res, poster_final: Path | None) -> None:
        """按首个海报候选 URL 直拉封面（绕过桌面版 OtherInfo 链）。失败静默。"""
        if not poster_final:
            return
        candidates = getattr(res, "poster_list", None) or []
        url = None
        if candidates:
            first = candidates[0]
            if isinstance(first, tuple) and len(first) >= 2:
                url = first[1]            # (site, url, is_available?)
            elif isinstance(first, dict):
                url = first.get("url")
            else:
                url = str(first)
        url = url or getattr(res, "poster", None)
        if not url:
            return
        import aiohttp
        from mdcx.config.manager import manager

        timeout = aiohttp.ClientTimeout(total=40)
        proxy = None
        try:
            if manager.config.use_proxy and manager.config.proxy:
                proxy = manager.config.proxy
        except Exception:  # noqa: BLE001
            pass
        poster_final.parent.mkdir(parents=True, exist_ok=True)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, proxy=proxy) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    await asyncio.to_thread(poster_final.write_bytes, data)
                    self._info(f"海报写入: {poster_final}")
                else:
                    self._info(f"海报下载 HTTP {resp.status}")