"""无头启动引导：必须先于任何 mdcx.config 导入执行。

关键约束（来自深入分析）：
- MAIN_PATH = /app（源码运行），MARK_FILE = /app/MDCx.config 内容是一行绝对路径，
  指向当前配置文件；该配置文件所在目录即"用户数据目录"。
- `import mdcx.config.manager` 时模块级 `manager = ConfigManager()` 会立即完成
  路径决议 + reset() + load()，所以标记文件必须在 import 前写好。
- PyQt6 在 core 链中被 import（signals/image/scraper/resources），但不创建 QApplication；
  设置 QT_QPA_PLATFORM=offscreen 作防御即可无头运行。
"""
from __future__ import annotations

import os
from pathlib import Path

from mdcx.consts import MARK_FILE

CONFIG_FILENAME = "config.json"


def bootstrap(data_dir: str | os.PathLike[str] | None = None, *, write_mark: bool = True) -> Path:
    data_dir = Path(data_dir or os.environ.get("MDCX_DATA_DIR", "/data")).expanduser().resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    config_file = data_dir / CONFIG_FILENAME
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if write_mark:
        # 与 docker/entrypoint.sh 一致：标记文件→数据目录/config.json
        try:
            MARK_FILE.parent.mkdir(parents=True, exist_ok=True)
            MARK_FILE.write_text(str(config_file), encoding="utf-8")
        except OSError:
            pass  # 只读容器也可运行（用默认位置）
    return config_file


def init_mdcx_once() -> None:
    """写入标记文件并按需触发 mdcx 核心模块初始化（幂等）。"""
    bootstrap()
    if "mdcx.config.manager" not in __import__("sys").modules:
        from mdcx.config.manager import manager  # noqa: F401  模块级单例：读/迁移/加载配置
    if "mdcx.config.resources" not in __import__("sys").modules:
        from mdcx.config.resources import resources  # noqa: F401  userdata 初始化