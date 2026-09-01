"""文件系统浏览（仅限挂载区 /media 及数据目录，防越权）。"""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Query

from ..settings import settings

router = APIRouter()

ALLOWED_ROOTS = [settings.media_dir, settings.data_dir]


def _safe(path: str) -> Path | None:
    p = Path(path).resolve()
    if p.is_symlink():
        return None
    for root in ALLOWED_ROOTS:
        root = root.resolve()
        if p == root or root in p.parents:
            return p
    return None


@router.get("/list")
async def list_dir(path: str = Query(default="/media")):
    p = _safe(path)
    if p is None:
        return {"ok": False, "error": "路径不在允许范围内"}
    if not p.is_dir():
        return {"ok": False, "error": "不是目录"}
    items = []
    try:
        for child in sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            try:
                st = child.stat()
            except OSError:
                continue
            items.append({
                "name": child.name,
                "is_dir": child.is_dir(),
                "is_link": child.is_symlink(),
                "size": st.st_size if child.is_file() else 0,
                "mtime": st.st_mtime,
            })
    except PermissionError:
        return {"ok": False, "error": "无权限读取"}
    return {"ok": True, "path": str(p), "items": items}