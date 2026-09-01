"""无头批量刮削引擎：复用 mdcx Scraper 全流程，信号→回调，取消走 Flags.stop_requested。

要点（来自核心链路分析）：
- Scraper.run(FileMode.Single, movie_list) 给定文件列表时跳过目录扫描，内部按
  config.thread_number 并发处理完整链路（爬取→翻译→命名→下载→写 nfo→移动）。
- 全局状态（manager/Flags）为进程单例，本服务在事件循环内串行运行批次。
- 进度：把 Qt 信号以 DirectConnection 直连到回调（同事件循环，无跨线程问题）。
- 取消：置 Flags.stop_requested → _check_stop 抛 StopScrape 优雅停止。
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

class HeadlessScrapeEngine:
    def __init__(self, on_progress: ProgressCb | None = None,
                 on_file: FileCb | None = None, on_log: LogCb | None = None) -> None:
        self.on_progress = on_progress
        self.on_file = on_file
        self.on_log = on_log
        self._hooked = False

    def _hook_signals(self) -> None:
        from PyQt6.QtCore import Qt
        from mdcx.signals import signal
        if self._hooked:
            return
        if self.on_progress is not None:
            signal.exec_set_processbar.connect(self._cb_pct, Qt.ConnectionType.DirectConnection)
        if self.on_file is not None:
            signal.set_label_file_path.connect(self._cb_file, Qt.ConnectionType.DirectConnection)
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
                         ("set_label_file_path", self._cb_file)):
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

    async def scrape_paths(self, paths: list[str]) -> dict:
        """刮削一批文件。返回汇总统计。"""
        from mdcx.config.manager import manager
        from mdcx.crawler import CrawlerProvider
        from mdcx.core.scraper import Scraper
        from mdcx.models.enums import FileMode
        from mdcx.models.flags import Flags

        movie_list = [Path(p) for p in paths]
        async with manager.acquire_computed() as computed:
            provider = CrawlerProvider(manager.config, computed.async_client,
                                       config_getter=lambda: manager.config)
            scraper = Scraper(provider)
            try:
                self._hook_signals()
                Flags.stop_requested = False
                await scraper.run(FileMode.Single, movie_list)
            finally:
                self._unhook_signals()
        return {
            "total": Flags.total_count,
            "done": Flags.scrape_done,
            "succ": Flags.succ_count,
            "fail": Flags.fail_count,
            "stopped": Flags.stop_requested,
        }

    @staticmethod
    def request_cancel() -> None:
        from mdcx.models.flags import Flags
        Flags.stop_requested = True