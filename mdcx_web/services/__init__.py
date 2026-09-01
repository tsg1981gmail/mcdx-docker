"""服务层公共设施：路径白名单、视频文件枚举、后台任务启动。"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Awaitable, Callable

from ..api.tasks import Task, TaskStatus, manager as task_manager
from ..settings import settings

log = logging.getLogger("mdcx.web")

VIDEO_EXTS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".ts", ".m2ts",
    ".rmvb", ".rm", ".webm", ".mpg", ".mpeg", ".3gp", ".vob", ".iso",
}

ALLOWED_ROOTS = [settings.media_dir, settings.data_dir]


def resolve_allowed(path: str | Path) -> Path | None:
    """解析并确认路径位于允许根（/media、/data）下，防越权访问宿主机其它目录。"""
    p = Path(path).expanduser().resolve()
    for root in ALLOWED_ROOTS:
        root = root.resolve()
        if p == root or root in p.parents:
            return p
    return None


def walk_videos(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    out: list[Path] = []
    try:
        for child in root.rglob("*"):
            if child.is_file() and child.suffix.lower() in VIDEO_EXTS:
                out.append(child)
    except OSError as exc:
        log.warning("walk %s failed: %s", root, exc)
    return sorted(out)


def fmt_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    if n < 1024 ** 3:
        return f"{n / 1024 ** 2:.1f} MB"
    return f"{n / 1024 ** 3:.2f} GB"


# 全局串行锁：mdcx 核心为进程级单例（manager/Flags/LogBuffer），并发批次会互相污染
_run_lock = asyncio.Lock()


async def start_task(
    kind: str,
    title: str,
    fn: Callable[[Task, asyncio.Event], Awaitable[Any]],
) -> str | None:
    """创建并启动后台任务。返回任务 id；已有任务在运行时返回 None（勿重复获取锁）。"""
    if _run_lock.locked():
        return None
    task = task_manager.create(kind, title)

    async def runner() -> None:
        task.status = TaskStatus.RUNNING
        task._atask = asyncio.current_task()
        try:
            result = await fn(task, task._cancel_event)
            task.status = TaskStatus.SUCCESS
            task.result = result
            task.progress = 100.0
        except asyncio.CancelledError:
            task.status = TaskStatus.CANCELLED
        except Exception as exc:  # noqa: BLE001
            log.exception("[%s] %s failed", task.id, title)
            task.status = TaskStatus.FAILED
            task.error = str(exc)
        finally:
            if _run_lock.locked():
                _run_lock.release()

    await _run_lock.acquire()
    asyncio.get_running_loop().create_task(runner())
    return task.id