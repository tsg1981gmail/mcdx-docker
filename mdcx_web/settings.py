"""mdcx-web 运行时配置（环境变量驱动，兼容 Docker/本地）。"""
from __future__ import annotations

import os
from pathlib import Path


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


class Settings:
    """容器/宿主机约定：
    - MDCX_DATA_DIR: 数据目录（config.json、缓存、日志）默认 /data
    - MDCX_MEDIA_DIR: 挂载区目录（/media = 宿主机挂载区，见部署）默认 /media
    - 配置文件: MDCX_DATA_DIR/config.json（与桌面版 mdcx ConfigManager 共用格式）
    """

    def __init__(self) -> None:
        self.data_dir = Path(_env("MDCX_DATA_DIR", "/data"))
        self.media_dir = Path(_env("MDCX_MEDIA_DIR", "/media"))
        self.static_dir = Path(__file__).resolve().parent.parent / "webui" / "dist"
        self.config_file = self.data_dir / "config.json"
        self.host = _env("MDCX_WEB_HOST", "0.0.0.0")
        self.port = int(_env("MDCX_WEB_PORT", "8000"))
        self.library_root = Path(_env("MDCX_LIBRARY_ROOT", "/media"))  # 整理目标库根目录（同盘硬链接前提）
        self.log_level = _env("MDCX_LOG_LEVEL", "INFO")

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()