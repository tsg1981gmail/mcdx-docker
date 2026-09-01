"""后台任务管理：内存任务表 + 轮询/SSE 进度。"""
from __future__ import annotations

import asyncio
import itertools
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: str
    kind: str
    title: str
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0  # 0-100
    detail: str = ""
    total: int = 0
    done: int = 0
    result: Any = None
    error: str = ""
    created: float = field(default_factory=time.time)
    updated: float = field(default_factory=time.time)
    cancel_requested: bool = False
    _cancel_event: asyncio.Event = field(default_factory=asyncio.Event, repr=False)

    def request_cancel(self) -> None:
        self.cancel_requested = True
        self._cancel_event.set()

    def update(self, done: int, total: int, detail: str = "") -> None:
        self.done, self.total = done, total
        self.progress = round(done * 100.0 / total, 1) if total else self.progress
        self.detail = detail
        self.updated = time.time()


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._ids = itertools.count(1)

    def create(self, kind: str, title: str) -> Task:
        task = Task(id=f"{kind}-{uuid.uuid4().hex[:8]}", kind=kind, title=title)
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list(self) -> list[dict]:
        return [self.snapshot(t) for t in sorted(self._tasks.values(), key=lambda x: x.created, reverse=True)]

    @staticmethod
    def snapshot(t: Task) -> dict:
        return {
            "id": t.id, "kind": t.kind, "title": t.title, "status": t.status.value,
            "progress": t.progress, "detail": t.detail, "total": t.total, "done": t.done,
            "error": t.error, "created": t.created, "updated": t.updated,
            "result": t.result,
        }

    def remove(self, task_id: str) -> None:
        self._tasks.pop(task_id, None)


manager = TaskManager()


@router.get("")
async def list_tasks():
    return {"ok": True, "tasks": manager.list()}


@router.get("/{task_id}")
async def get_task(task_id: str):
    t = manager.get(task_id)
    if not t:
        return {"ok": False, "error": "任务不存在"}
    return {"ok": True, "task": manager.snapshot(t)}


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    t = manager.get(task_id)
    if not t:
        return {"ok": False, "error": "任务不存在"}
    t.request_cancel()
    # tools 类任务无内建优雅停止点 → 直接取消底层协程（crawl 走 Flags 优雅停止）
    atask = getattr(t, "_atask", None)
    if t.kind == "tools" and atask is not None and not atask.done():
        try:
            atask.cancel()
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


@router.post("/{task_id}/remove")
async def remove_task(task_id: str):
    manager.remove(task_id)
    return {"ok": True}


@router.get("/events")
async def task_events():
    """简单 SSE 轮询推送。"""

    async def gen():
        last = 0.0
        while True:
            tasks = manager.list()
            now = max((t["updated"] for t in tasks), default=0.0)
            if now != last:
                last = now
                yield f"data: {tasks!s}\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(gen(), media_type="text/event-stream")