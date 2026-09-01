"""网络检测 API（对应原版 page_net：检测各网站连通性与代理）。"""
from __future__ import annotations

import asyncio
import time

from fastapi import APIRouter

router = APIRouter()

PROBE_SITES = [
    ("javbus", "https://www.javbus.com/"),
    ("javdb", "https://javdb.com/"),
    ("dmm", "https://www.dmm.co.jp/"),
    ("missav", "https://missav.com/"),
    ("avmoo", "https://avmoo.ong/"),
    ("theporndb", "https://www.theporndb.com/"),
    ("jav321", "https://www.jav321.com/"),
    ("fc2hub", "https://fc2hub.com/"),
]


def _proxy_of(config) -> str | None:
    try:
        if config.use_proxy and config.proxy:
            return config.proxy
    except Exception:  # noqa: BLE001
        pass
    return None


async def _probe(session, url: str, proxy: str | None, timeout: float = 8.0) -> tuple[int | None, float, str]:
    t0 = time.monotonic()
    try:
        async with session.get(url, proxy=proxy, timeout=timeout) as resp:
            return resp.status, (time.monotonic() - t0) * 1000, ""
    except Exception as exc:  # noqa: BLE001
        return None, (time.monotonic() - t0) * 1000, str(exc)[:80]


@router.post("/check")
async def check_network():
    import aiohttp
    from mdcx.config.manager import manager

    proxy = _proxy_of(manager.config)
    timeout = aiohttp.ClientTimeout(total=12)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        results = await asyncio.gather(*[_probe(session, url, proxy) for _, url in PROBE_SITES])
    items = []
    for (name, url), (status, ms, err) in zip(PROBE_SITES, results):
        items.append({
            "site": name, "url": url, "status": status,
            "time_ms": round(ms, 1),
            "error": err,
            "ok": status is not None and status < 400,
        })
    # 代理本身连通性
    p_ok = None
    if proxy:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as s:
                async with s.get("https://cloudflare.com", proxy=proxy, timeout=8) as r:
                    p_ok = r.status
        except Exception:  # noqa: BLE001
            p_ok = None
    return {
        "ok": True,
        "proxy": proxy,
        "proxy_reachable": p_ok is not None,
        "items": items,
        "summary": {"ok": sum(1 for i in items if i["ok"]), "fail": sum(1 for i in items if not i["ok"])},
        "note": "代理可达时建议在设置-网络中启用并勾选全部走代理",
    }