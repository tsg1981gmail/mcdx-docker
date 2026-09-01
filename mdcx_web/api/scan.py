"""目录扫描 API：枚举 /media 挂载区下的视频文件。"""
from __future__ import annotations

import time

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import fmt_size, resolve_allowed, walk_videos

router = APIRouter()


class ScanRequest(BaseModel):
    path: str = "/media"
    deep: bool = True
    limit: int = 3000


@router.post("/scan")
async def scan_videos(req: ScanRequest):
    root = resolve_allowed(req.path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围（/media 或 /data）"}
    if not root.is_dir():
        return {"ok": False, "error": "不是目录"}
    videos = walk_videos(root)
    items = []
    for p in videos[: req.limit]:
        try:
            st = p.stat()
        except OSError:
            continue
        items.append({
            "path": str(p),
            "name": p.name,
            "dir": str(p.parent),
            "size": st.st_size,
            "size_h": fmt_size(st.st_size),
            "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)),
        })
    return {
        "ok": True,
        "root": str(root),
        "found": len(videos),
        "listed": len(items),
        "truncated": len(videos) > req.limit,
        "items": items,
    }