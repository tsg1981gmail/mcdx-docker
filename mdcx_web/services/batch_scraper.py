"""无头批量刮削引擎：复用 mdcx Scraper 全流程，信号→回调，取消走 Flags.stop_requested。

要点（来自核心链路分析）：
- Scraper.run(FileMode, movie_list) 给定文件列表时跳过目录扫描，内部按
  config.thread_number 并发处理完整链路（爬取→翻译→命名→下载→写 nfo→移动）。
- 刮削模式与原版 1:1：config.main_mode 1 正常 / 2 整理 / 3 更新 / 4 读取；
  单文件强制重刮用 FileMode.Again。引擎按 mode 设置 main_mode（跑完还原）。
- 三列表收集：signal.exec_show_list_name("succ"|"fail", ShowData, number) 直连回调；
  success.txt / remain.txt 为持久化成功/剩余列表（刮削后读取）。
- 全局状态（manager/Flags）为进程单例，本服务在事件循环内串行运行批次。
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Awaitable, Callable

log = logging.getLogger("mdcx.web")

ProgressCb = Callable[[int, int, int, int], None]   # (done, total, succ, fail)
FileCb = Callable[[str], None]
LogCb = Callable[[str], None]

MODE_MAIN = {"common": 1, "sort": 2, "update": 3, "read": 4}

class HeadlessScrapeEngine:
    def __init__(self, on_progress: ProgressCb | None = None,
                 on_file: FileCb | None = None, on_log: LogCb | None = None) -> None:
        self.on_progress = on_progress
        self.on_file = on_file
        self.on_log = on_log
        self._hooked = False
        self.records: list[dict] = []   # 单次运行的 成功/失败 记录

    def _hook_signals(self) -> None:
        from PyQt6.QtCore import Qt
        from mdcx.signals import signal
        if self._hooked:
            return
        if self.on_progress is not None:
            signal.exec_set_processbar.connect(self._cb_pct, Qt.ConnectionType.DirectConnection)
        if self.on_file is not None:
            signal.set_label_file_path.connect(self._cb_file, Qt.ConnectionType.DirectConnection)
        # 收集 成功/失败 列表（原版界面右侧三列表的数据源）
        signal.exec_show_list_name.connect(self._cb_list_name, Qt.ConnectionType.DirectConnection)
        if self.on_log is not None:
            signal.show_web_log.connect(self._cb_log, Qt.ConnectionType.DirectConnection) \
                if hasattr(signal, "show_web_log") else None
            self._orig_show_log = signal.show_log_text
            signal.show_log_text = self._wrap_log
        self._hooked = True

    def _unhook_signals(self) -> None:
        from mdcx.signals import signal
        if not self._hooked:
            return
        # pyqtSignal.disconnect 无接收者时可能抛 RuntimeError，尽量安全
        for attr, cb in (("exec_set_processbar", self._cb_pct),
                         ("set_label_file_path", self._cb_file),
                         ("exec_show_list_name", self._cb_list_name)):
            try:
                sig = getattr(signal, attr)
                try:
                    sig.disconnect(cb)
                except Exception:  # noqa: BLE001
                    pass
            except Exception:  # noqa: BLE001
                pass
        self._hooked = False

    def _cb_pct(self, pct: int) -> None:
        if self.on_progress:
            from mdcx.models.flags import Flags
            self.on_progress(Flags.scrape_done, Flags.total_count, Flags.succ_count, Flags.fail_count)

    def _cb_file(self, path: str) -> None:
        if self.on_file:
            self.on_file(path)

    def _cb_log(self, text: str) -> None:  # type: ignore[override]
        if self.on_log:
            self.on_log(text)

    def _wrap_log(self, text: str) -> None:
        if self.on_log:
            self.on_log(text)

    def _cb_list_name(self, status: str, show_data, number: str) -> None:
        """status ∈ {'succ','fail'}；show_data: ShowData（含 show_name/title 等）。"""
        self.records.append({
            "status": status,
            "number": str(number or ""),
            "show_name": getattr(show_data, "show_name", "") if show_data is not None else "",
            "title": getattr(show_data, "title", "") if show_data is not None else "",
        })

    @staticmethod
    def _read_list(name: str) -> list[str]:
        from mdcx.config.manager import manager
        from mdcx.config.resources import resources
        path = resources.u(name)
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            return [ln.strip() for ln in lines if ln.strip()]
        except OSError:
            return []

    async def scrape_paths(self, paths: list[str], mode: str = "common", *,
                           force: bool = False) -> dict:
        """按原版模式刮削一批文件。mode: common|sort|update|read；force=单文件强制重刮(FileMode.Again)。"""
        from mdcx.config.manager import manager
        from mdcx.crawler import CrawlerProvider
        from mdcx.core.scraper import Scraper
        from mdcx.models.enums import FileMode
        from mdcx.models.flags import Flags

        movie_list = [Path(p) for p in paths]
        self.records = []
        old_main = getattr(manager.config, "main_mode", 1)
        new_main = MODE_MAIN.get(mode, old_main)
        file_mode = FileMode.Again if force else FileMode.Default

        async with manager.acquire_computed() as computed:
            provider = CrawlerProvider(manager.config, computed.async_client,
                                       config_getter=lambda: manager.config)
            scraper = Scraper(provider)
            try:
                if new_main != old_main:
                    manager.config.main_mode = new_main
                Flags.stop_requested = False
                self._hook_signals()
                try:
                    await scraper.run(file_mode, movie_list)
                finally:
                    self._unhook_signals()
            finally:
                if new_main != old_main:
                    manager.config.main_mode = old_main
        return {
            "total": Flags.total_count,
            "done": Flags.scrape_done,
            "succ": Flags.succ_count,
            "fail": Flags.fail_count,
            "stopped": Flags.stop_requested,
            "mode": mode,
            "records": self.records,
            "success_list": self._read_list("success.txt"),
            "remain_list": self._read_list("remain.txt"),
        }

    @staticmethod
    def request_cancel() -> None:
        from mdcx.models.flags import Flags
        Flags.stop_requested = True