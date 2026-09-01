"""mdcx-web 应用工厂与启动入口。

启动顺序（重要）：先 bootstrap（写 MDCx.config 标记文件）+ 初始化 mdcx 核心，
再创建 FastAPI。退出时 flush TMDB 缓存并释放 computed 异步客户端。
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .api.routers import api_router
from .bootstrap import bootstrap, init_mdcx_once
from .settings import settings

log = logging.getLogger("mdcx.web")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    try:
        from mdcx.core.tmdb_actor import flush_tmdb_query_cache

        flush_tmdb_query_cache()
    except Exception as exc:  # noqa: BLE001
        log.warning("flush tmdb cache failed: %s", exc)
    try:
        from mdcx.config.manager import manager

        if getattr(manager, "computed", None) is not None:
            await manager.computed.close()
    except Exception as exc:  # noqa: BLE001
        log.warning("close computed failed: %s", exc)


def create_app() -> FastAPI:
    bootstrap(settings.data_dir)
    settings.ensure_dirs()
    init_mdcx_once()

    app = FastAPI(
        title="mdcx-web",
        description="基于 mdcx-diy 核心的视频刮削与整理 Web 应用",
        version="0.1.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix="/api")

    @app.exception_handler(Exception)
    async def unhandled(_request, exc: Exception):
        log.exception("unhandled error: %s", exc)
        return JSONResponse(status_code=500, content={"ok": False, "error": str(exc)})

    if settings.static_dir.is_dir():
        app.mount("/", StaticFiles(directory=str(settings.static_dir), html=True), name="static")
    else:
        @app.get("/", include_in_schema=False)
        async def index_note():
            return {"ok": True, "note": "前端未构建。在 webui/ 执行 npm install && npm run build 后重启。"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=settings.log_level)
    uvicorn.run("mdcx_web.main:app", host=settings.host, port=settings.port, reload=False)