"""NFO 库 API（对应原版 page_nfo_library：批量浏览/读取/编辑/重写 NFO）。"""
from __future__ import annotations

import asyncio
import re
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..services import resolve_allowed, start_task

router = APIRouter()


def _list_nfo(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*.nfo") if p.is_file())


@router.get("/list")
async def nfo_list(path: str, filter_text: str = ""):
    root = resolve_allowed(path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}
    items = []
    for p in _list_nfo(root):
        number = p.stem
        if filter_text and filter_text.lower() not in number.lower():
            continue
        try:
            st = p.stat()
            size = st.st_size
        except OSError:
            size = 0
        items.append({"path": str(p), "number": number, "parent": str(p.parent), "size": size})
    return {"ok": True, "count": len(items), "items": items}


@router.get("/read")
async def nfo_read(path: str):
    root = resolve_allowed(path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}
    p = Path(path).resolve()
    if not p.is_file() or p.suffix.lower() != ".nfo":
        return {"ok": False, "error": "不是 nfo 文件"}

    def _parse() -> dict:
        from lxml import etree
        text = p.read_text(encoding="utf-8", errors="ignore")
        fields: dict[str, str] = {}
        try:
            root_el = etree.fromstring(text.encode("utf-8", errors="ignore"))
            for child in root_el:
                tag = child.tag.split("}")[-1]
                if child.text:
                    fields.setdefault(tag, child.text.strip())
        except Exception:
            pass
        return {"raw": text, "fields": fields}

    d = await asyncio.to_thread(_parse)
    return {"ok": True, "path": str(p), "number": p.stem, **_parse()}


class NfoPatchRequest(BaseModel):
    path: str
    fields: dict[str, str] = {}
    number: str = ""
    title: str = ""
    actors: list[str] = []
    outline: str = ""
    year: str = ""
    release: str = ""
    studio: str = ""
    tags: list[str] = []


@router.post("/patch")
async def nfo_patch(req: NfoPatchRequest):
    root = resolve_allowed(req.path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}
    p = Path(req.path).resolve()
    if not p.is_file() or p.suffix.lower() != ".nfo":
        return {"ok": False, "error": "不是 nfo 文件"}

    def _rewrite() -> str:
        from lxml import etree
        tree = etree.parse(str(p))
        r = tree.getroot()
        ns_prefix = None
        if r.nsmap:
            ns_prefix = "{%s}" % (list(r.nsmap.values())[0])

        def set_text(tag: str, value: str | None) -> None:
            if value is None:
                return
            el = r.find(f"{ns_prefix}{tag}") if ns_prefix else r.find(tag)
            if el is not None:
                el.text = value
            else:
                # 原节点不存在则新建（在父链尾追加）
                new_el = etree.SubElement(r, tag)
                new_el.text = value
                if ns_prefix:
                    new_el.tag = f"{ns_prefix}{tag}"
        if req.number: set_text("number", req.number)
        if req.title: set_text("title", req.title)
        if req.outline: set_text("outline", req.outline)
        if req.year: set_text("year", req.year)
        if req.release: set_text("release", req.release)
        if req.studio: set_text("studio", req.studio)
        for k, v in req.fields.items():
            if k in ("number", "title", "outline", "year", "release", "studio"):
                continue
            set_text(k, v)
        data = etree.tostring(tree, encoding="UTF-8", xml_declaration=True, pretty_print=True)
        p.write_bytes(data)
        return p.read_text(encoding="utf-8")[:500]

    try:
        preview = await asyncio.to_thread(_rewrite)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "preview": preview}


class NfoDeleteRequest(BaseModel):
    path: str


@router.post("/delete")
async def nfo_delete(req: NfoDeleteRequest):
    root = resolve_allowed(req.path)
    if root is None:
        return {"ok": False, "error": "路径不在允许范围"}
    p = Path(req.path).resolve()
    if not p.is_file():
        return {"ok": False, "error": "不是文件"}
    try:
        p.unlink()
    except OSError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True}