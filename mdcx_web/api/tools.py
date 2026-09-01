"""工具 API：映射原版 page_tool 的 8 个面板 + Gfriends 同步。"""
from __future__ import annotations

import asyncio
import logging
import shutil
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import resolve_allowed, start_task

log = logging.getLogger("mdcx.web")
router = APIRouter()

TOOLS_INDEX = [
    {"key": "single_scrape", "name": "单文件刮削（指定番号网址）", "ready": True},
    {"key": "poster_cut", "name": "裁剪图片（封面图比例，可选水印）", "ready": True},
    {"key": "missing", "name": "检查演员缺失番号", "ready": True},
    {"key": "move_videos", "name": "移动视频、字幕", "ready": True},
    {"key": "symlink_helper", "name": "软链接助手", "ready": True},
    {"key": "actor_db", "name": "演员库维护", "ready": True},
    {"key": "cover_backfill", "name": "封面补图", "ready": True},
    {"key": "scrape_cache", "name": "刮削缓存管理（断点续刮/失败重试）", "ready": True},
    {"key": "sync_gfriends", "name": "Gfriends 同步", "ready": True},
]


@router.get("")
async def tools_index():
    return {"ok": True, "tools": TOOLS_INDEX}


# ---------- 刮削缓存管理 ----------
class CacheActionRequest(BaseModel):
    action: str  # list | clear


async def _state_db_path() -> Path:
    from mdcx.config.resources import resources
    return resources.u("scrape_state.db")


@router.post("/cache")
async def scrape_cache(req: CacheActionRequest):
    from mdcx.config.resources import resources

    db = await _state_db_path()
    if req.action == "clear":
        try:
            db.unlink(missing_ok=True)
        except OSError as exc:
            return {"ok": False, "error": str(exc)}
    succ = resources.u("success.txt")
    remain = resources.u("remain.txt")
    counts = {}
    for name, p in (("success", succ), ("remain", remain)):
        try:
            counts[name] = len([ln for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()])
        except OSError:
            counts[name] = 0
    return {"ok": True, "db_exists": db.exists(), "db_path": str(db),
            "success_count": counts["success"], "remain_count": counts["remain"]}


# ---------- 移动视频、字幕（复刻原版 _move_files_core 语义）----------
class MoveVideosRequest(BaseModel):
    path: str
    target_dir: str = "Movie_moved"


@router.post("/move-videos")
async def move_videos(req: MoveVideosRequest):
    root = resolve_allowed(req.path)
    if root is None or not root.is_dir():
        return {"ok": False, "error": "路径不在允许范围或不是目录"}

    SUBS = {".srt", ".ass", ".ssa", ".sub", ".idx"}
    VID = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".ts", ".m2ts", ".rmvb", ".webm", ".mpg", ".mpeg", ".vob"}
    target = (root / req.target_dir).resolve()
    target.mkdir(parents=True, exist_ok=True)

    async def worker(_task, stop):
        moved = []
        for child in sorted(root.iterdir()):
            if stop.is_set():
                break
            if child.is_file() and child.suffix.lower() in VID:
                dst = target / child.name
                if not dst.exists():
                    shutil.move(str(child), str(dst))
                    moved.append(str(dst))
        for child in sorted(root.iterdir()):
            if child.is_file() and child.suffix.lower() in SUBS:
                dst = target / child.name
                if not dst.exists():
                    shutil.move(str(child), str(dst))
                    moved.append(str(dst))
        return {"moved": len(moved), "target": str(target), "samples": moved[:20]}

    tid = await start_task("tools", f"移动视频字幕 → {req.target_dir}", worker)
    if tid is None:
        return {"ok": False, "error": "已有任务在运行"}
    return {"ok": True, "task_id": tid}


# ---------- 软链接助手 ----------
class SymlinkHelperRequest(BaseModel):
    netdisk_path: str
    local_path: str
    copy_files: bool = False


@router.post("/symlink-helper")
async def symlink_helper(req: SymlinkHelperRequest):
    net = resolve_allowed(req.netdisk_path)
    local = resolve_allowed(req.local_path)
    if net is None or local is None:
        return {"ok": False, "error": "路径不在允许范围"}
    if not net.is_dir() or not local.is_dir():
        return {"ok": False, "error": "需要已存在的目录"}

    async def worker(_task, stop):
        from mdcx.base.file import newtdisk_creat_symlink
        await newtdisk_creat_symlink(req.copy_files, netdisk_path=net, local_path=local)
        return {"ok": True}

    tid = await start_task("tools", "软链接助手", worker)
    if tid is None:
        return {"ok": False, "error": "已有任务在运行"}
    return {"ok": True, "task_id": tid}


# ---------- 裁剪图片（PIL：居中 2:3 封面裁剪，纯本地）----------
class PosterCutRequest(BaseModel):
    image: str
    out: str
    ratio_w: float = 2
    ratio_h: float = 3


@router.post("/poster-cut")
async def poster_cut(req: PosterCutRequest):
    src = resolve_allowed(req.image)
    dst = resolve_allowed(req.out)
    if src is None or dst is None:
        return {"ok": False, "error": "路径不在允许范围"}
    if not src.is_file():
        return {"ok": False, "error": "图片不存在"}

    def _cut() -> None:
        from PIL import Image
        img = Image.open(src)
        w, h = img.size
        target_ratio = req.ratio_w / req.ratio_h
        cur_ratio = w / h
        if cur_ratio > target_ratio:   # 太宽：裁左右
            new_w = int(h * target_ratio)
            x = (w - new_w) // 2
            box = (x, 0, x + new_w, h)
        else:                           # 太高：裁上下（偏上）
            new_h = int(w / target_ratio)
            y = 0
            box = (0, y, w, y + new_h)
        img = img.crop(box)
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, quality=92)

    try:
        await asyncio.to_thread(_cut)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "out": str(dst)}


# ---------- 演员库维护（映射原版演员库维护面板按钮）----------
class ActorDbRequest(BaseModel):
    action: str     # clean_male | verify_tmdb_ids | sync_from_avdb | update_nfo_tmdb_ids
    nfo_dir: str = ""


@router.post("/actor-db")
async def actor_db(req: ActorDbRequest):
    actions = {
        "clean_male": lambda: _actor_fn("clean_male_actors"),
        "verify_tmdb_ids": lambda: _actor_fn("verify_tmdb_ids"),
        "sync_from_avdb": lambda: _actor_fn("sync_from_avdb"),
        "update_nfo_tmdb_ids": lambda: _actor_fn("update_nfo_tmdb_ids", req.nfo_dir),
    }
    fn = actions.get(req.action)
    if fn is None:
        return {"ok": False, "error": "未知动作"}

    async def worker(_task, stop):
        return await fn()

    tid = await start_task("tools", f"演员库维护·{req.action}", worker)
    if tid is None:
        return {"ok": False, "error": "已有任务在运行"}
    return {"ok": True, "task_id": tid}


async def _actor_fn(name: str, nfo_dir: str = ""):
    from importlib import import_module
    mod = import_module("mdcx.tools.actor_db_tool")
    fn = getattr(mod, name)
    if name == "update_nfo_tmdb_ids":
        p = resolve_allowed(nfo_dir)
        if p is None:
            return {"ok": False, "error": "nfo_dir 不在允许范围"}
        result = await fn(p)
    else:
        result = await fn()
    import dataclasses
    if dataclasses.is_dataclass(result):
        result = dataclasses.asdict(result)
    return result


# ---------- 检查演员缺失番号 ----------
class MissingRequest(BaseModel):
    actors_name: str = ""
    local_library: list[str] = []
    deep: bool = True


@router.post("/missing")
async def missing(req: MissingRequest):
    from mdcx.config.manager import manager
    from mdcx.signals import signal

    logs: list[str] = []

    async def worker(_task, stop):
        old_an = manager.config.actors_name
        old_ll = list(manager.config.local_library or [])
        try:
            if req.actors_name:
                manager.config.actors_name = req.actors_name
            if req.local_library:
                manager.config.local_library = req.local_library
            from mdcx.tools.missing import check_missing_number

            orig = signal.show_log_text
            def cap(text: str) -> None:
                logs.append(text)
                orig(text)
            signal.show_log_text = cap
            try:
                await check_missing_number(req.deep)
            finally:
                signal.show_log_text = orig
        finally:
            manager.config.actors_name = old_an
            manager.config.local_library = old_ll
        return {"log_lines": len(logs), "logs": logs[-150:]}

    tid = await start_task("tools", "检查演员缺失番号", worker)
    if tid is None:
        return {"ok": False, "error": "已有任务在运行"}
    return {"ok": True, "task_id": tid}


# ---------- 封面补图（原版脚本 backfill_cover，按番号补齐海报/缩略图）----------
class CoverBackfillRequest(BaseModel):
    numbers: str = ""
    overwrite: bool = False
    watermark: bool = True


@router.post("/cover-backfill")
async def cover_backfill(req: CoverBackfillRequest):
    from mdcx.config.manager import manager
    from mdcx.signals import signal

    number_list = [n.strip() for n in req.numbers.replace(",", " ").split() if n.strip()]
    if not number_list:
        return {"ok": False, "error": "请输入番号"}
    logs: list[str] = []

    async def worker(_task, stop):
        from scripts.cover_backfill import backfill_cover

        orig = signal.show_log_text
        def cap(text: str) -> None:
            logs.append(text)
            orig(text)
        signal.show_log_text = cap
        try:
            results = []
            for number in number_list:
                if stop.is_set():
                    break
                cap(f"开始补图: {number}")
                try:
                    result = await backfill_cover(
                        number, output_dir=manager.data_folder,
                        overwrite=req.overwrite, watermark=req.watermark,
                    )
                    results.append({"number": number, "result": result})
                except Exception as exc:  # noqa: BLE001
                    cap(f"补图失败 {number}: {exc}")
                    results.append({"number": number, "result": None, "error": str(exc)})
        finally:
            signal.show_log_text = orig
        return {"results": results, "log_lines": len(logs), "logs": logs[-150:]}

    tid = await start_task("tools", f"封面补图 {len(number_list)} 部", worker)
    if tid is None:
        return {"ok": False, "error": "已有任务在运行"}
    return {"ok": True, "task_id": tid}


# ---------- Gfriends ----------
class SyncGfriendsRequest(BaseModel):
    path: str = "/data/userdata/gfriends"


@router.post("/sync-gfriends")
async def sync_gfriends(req: SyncGfriendsRequest):
    from ..services import resolve_allowed

    root = resolve_allowed(req.path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}

    async def worker(_task, stop):
        from mdcx.tools.sync_gfriends import sync_gfriends as _sync
        ok, msg = await asyncio.to_thread(_sync, local_path=str(root))
        return {"ok": ok, "message": msg}

    tid = await start_task("tools", "Gfriends 同步", worker)
    if tid is None:
        return {"ok": False, "error": "已有任务在运行"}
    return {"ok": True, "task_id": tid}