"""路由注册。业务实现随后续模块落地逐步替换占位。"""
from __future__ import annotations

from fastapi import APIRouter

from . import config as config_api
from . import crawl as crawl_api
from . import files as files_api
from . import net as net_api
from . import nfo_library as nfo_api
from . import organize as organize_api
from . import scan as scan_api
from . import tasks as tasks_api
from . import tools as tools_api

api_router = APIRouter()
api_router.include_router(tasks_api.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(config_api.router, prefix="/config", tags=["config"])
api_router.include_router(files_api.router, prefix="/files", tags=["files"])
api_router.include_router(scan_api.router, prefix="/scan", tags=["scan"])
api_router.include_router(net_api.router, prefix="/net", tags=["net"])
api_router.include_router(crawl_api.router, prefix="/crawl", tags=["crawl"])
api_router.include_router(organize_api.router, prefix="/organize", tags=["organize"])
api_router.include_router(tools_api.router, prefix="/tools", tags=["tools"])
api_router.include_router(nfo_api.router, prefix="/nfo", tags=["nfo"])


@api_router.get("/system/health")
async def health():
    return {"ok": True, "service": "mdcx-web", "version": "0.1.0"}