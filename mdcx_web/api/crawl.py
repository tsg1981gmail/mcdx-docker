"""批量刮削 API：提交任务、预览文件列表、查看进度/结果。"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import (
    resolve_allowed,
    start_task,
    walk_videos,
)
from ..services.batch_scraper import HeadlessScrapeEngine

log = logging.getLogger("mdcx.web")
router = APIRouter()


class CrawlStartRequest(BaseModel):
    path: str | None = None      # 目录：递归枚举视频
    files: list[str] = []        # 或显式文件列表
    title: str = "批量刮削"


@router.get("/preview")
async def crawl_preview(path: str = "/media"):
    root = resolve_allowed(path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}
    videos = walk_videos(root) if root.is_dir() else []
    return {
        "ok": True,
        "path": str(root),
        "count": len(videos),
        "sample": [str(v) for v in videos[:50]],
    }


@router.post("/start")
async def start_crawl(req: CrawlStartRequest):
    files = [Path(f) for f in req.files if f]
    if req.path:
        root = resolve_allowed(req.path)
        if root is None:
            return {"ok": False, "error": "路径不在允许范围（/media 或 /data）"}
        files = walk_videos(root)
    elif not files:
        return {"ok": False, "error": "请提供 path 或 files"}
    if not files:
        return {"ok": False, "error": "该目录下没有视频文件"}

    paths = [str(f) for f in files]
    engine = HeadlessScrapeEngine()

    async def worker(task, stop):
        async def watch():
            await stop.wait()
            HeadlessScrapeEngine.request_cancel()

        watcher = asyncio.create_task(watch())
        try:
            result = await engine.scrape_paths(paths)
        finally:
            watcher.cancel()
        return result

    # 进度回填
    async def _run_with_progress(task, stop):
        from mdcx.config.manager import manager  # noqa: F401  (确保接线)

        engine.on_progress = lambda done, total, succ, fail: (
            task.update(done, total or 1, f"成功 {succ} / 失败 {fail}")
        )
        engine.on_file = lambda f: setattr(task, "detail", f"处理中: {Path(f).name}")
        task.total = len(paths)
        return await worker(task, stop)

    task_id = await start_task("crawl", req.title, _run_with_progress)
    if task_id is None:
        return {"ok": False, "error": "已有任务在运行，请等待完成或取消后重试"}
    return {"ok": True, "task_id": task_id, "count": len(paths)}