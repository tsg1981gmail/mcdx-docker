"""工具 API：按 mdcx/tools 无头化逐步接入。v1：Gfriends 同步；其余待后续。"""
from __future__ import annotations

import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

TOOLS_INDEX = [
    {"key": "actor_db", "name": "演员库工具", "ready": False},
    {"key": "subtitle", "name": "字幕检查", "ready": False},
    {"key": "missing", "name": "缺失检查", "ready": False},
    {"key": "emby_actor", "name": "Emby 演员管理", "ready": False},
    {"key": "wiki", "name": "Wiki 演员刮削", "ready": False},
    {"key": "sync_gfriends", "name": "Gfriends 同步", "ready": True},
]


@router.get("")
async def tools_index():
    return {"ok": True, "tools": TOOLS_INDEX}


class SyncGfriendsRequest(BaseModel):
    path: str = "/data/userdata/gfriends"


@router.post("/sync-gfriends")
async def sync_gfriends(req: SyncGfriendsRequest):
    from ..services import resolve_allowed

    root = resolve_allowed(req.path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}

    def _run() -> tuple[bool, str]:
        from mdcx.tools.sync_gfriends import sync_gfriends as _sync

        return _sync(local_path=str(root))

    ok, msg = await asyncio.to_thread(_run)
    return {"ok": ok, "message": msg}