"""整理 API：源目录 → 目标库 硬链接/复制 整理任务。"""
from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import resolve_allowed, start_task, walk_videos
from ..services.organizer import Organizer

router = APIRouter()


class OrganizeStartRequest(BaseModel):
    source: str = "/media/movies"
    library: str = "/media/library"
    mode: str = "hardlink"          # hardlink | copy
    concurrency: int = 4
    download_poster: bool = True
    title: str = "整理（硬链接/复制）"


@router.post("/preview")
async def organize_preview(req: OrganizeStartRequest):
    src = resolve_allowed(req.source)
    lib = resolve_allowed(req.library)
    if src is None or lib is None:
        return {"ok": False, "error": "源或目标路径不在允许范围"}
    if not src.is_dir():
        return {"ok": False, "error": "源目录不存在"}
    lib.mkdir(parents=True, exist_ok=True)
    videos = walk_videos(src)
    same_fs = None
    if videos:
        try:
            same_fs = os.stat(videos[0]).st_dev == os.stat(lib).st_dev
        except OSError:
            same_fs = False
    return {
        "ok": True,
        "count": len(videos),
        "same_filesystem": same_fs,
        "note": "同文件系统可使用硬链接；跨盘将自动回退复制。" if not same_fs else "硬链接可用（同文件系统）。",
        "first": [str(v) for v in videos[:20]],
    }


@router.post("/start")
async def start_organize(req: OrganizeStartRequest):
    src = resolve_allowed(req.source)
    lib = resolve_allowed(req.library)
    if src is None or lib is None:
        return {"ok": False, "error": "源或目标路径不在允许范围"}
    if not src.is_dir():
        return {"ok": False, "error": "源目录不存在"}
    videos = walk_videos(src)
    if not videos:
        return {"ok": False, "error": "源目录下没有视频文件"}

    organizer = Organizer(lib, mode=req.mode, download_poster=req.download_poster)
    concurrency = max(1, min(req.concurrency, 8))

    async def worker(task, stop):
        items = await organizer.organize_paths(videos, concurrency=concurrency, stop=stop)
        summary = {"total": len(items), "linked": 0, "copied": 0, "skipped": 0,
                   "failed": 0, "no_meta": 0, "items": []}
        for it in items:
            summary[it.action] = summary.get(it.action, 0) + 1
            if it.action == "failed":
                summary["failures"] = summary.get("failures", [])
                summary["failures"].append({"src": it.src, "detail": it.detail})
        # 结果明细太长只留失败项 + 摘要
        summary.pop("items", None)
        return summary

    async def _run_with_progress(task, stop):
        organizer.on_progress = lambda done, total: (
            task.update(done, total, f"{done}/{total}")
        )
        task.total = len(videos)
        return await worker(task, stop)

    task_id = await start_task("organize", req.title, _run_with_progress)
    if task_id is None:
        return {"ok": False, "error": "已有任务在运行，请等待完成或取消后重试"}
    return {"ok": True, "task_id": task_id, "count": len(videos)}