"""配置 API：读写 /data/config.json（mdcx ConfigManager 四步法 + 脱敏）。"""
from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..settings import settings

router = APIRouter()

_PRESET_NAME_RE = re.compile(r"^[\w\u4e00-\u9fa5 -]{1,40}$")


@router.get("")
async def get_config():
    from mdcx.config.manager import manager

    return {
        "ok": True,
        "config": manager.config.model_dump(mask_secrets=True),
        "config_path": str(manager.path),
        "data_folder": str(manager.data_folder),
        "web": {"data_dir": str(settings.data_dir), "media_dir": str(settings.media_dir)},
    }


@router.put("")
async def put_config(payload: dict):
    """合并式更新：只覆盖 payload 中的键（保护敏感字段不被打码值回写），再四步法落盘。"""
    from mdcx.config.manager import manager
    from mdcx.config.models import Config

    try:
        # 用内存中的真实配置做基底（未打码），仅应用 payload 提供的键
        base = manager.config.model_dump(mask_secrets=False)
        _merge_dict(base, payload)
        errors = Config.update(base)
        cfg = Config.model_validate(base)
        manager._replace_config(cfg)
        manager.save()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"配置校验失败: {exc}"}
    return {"ok": True, "errors": errors or [], "config_path": str(manager.path)}


def _merge_dict(base: dict, patch: dict) -> None:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge_dict(base[k], v)
        else:
            base[k] = v


# ==================== 配置方案（预设）管理 ====================
# 原理：mdcx ConfigManager 原生支持多配置文件（data_folder 下多个 .json，
# 通过 MARK_FILE 指向激活的那个，list_configs 列出全部）。


class PresetCreateRequest(BaseModel):
    name: str
    base: str = "config.json"    # 从哪个方案复制（默认当前激活方案）


class PresetSwitchRequest(BaseModel):
    name: str


class PresetDeleteRequest(BaseModel):
    name: str


def _preset_path(name: str) -> Path:
    from mdcx.config.manager import manager
    return manager.data_folder / (name if name.endswith(".json") else f"{name}.json")


@router.get("/presets")
async def list_presets():
    from mdcx.config.manager import manager
    try:
        items = manager.list_configs()
    except Exception:  # noqa: BLE001
        items = []
    presets = []
    for name in items:
        if name.endswith(".json"):
            presets.append({"name": name, "active": manager.path.name == name,
                            "label": name[:-5] if name != "config.json" else "默认"})
    return {"ok": True, "presets": presets, "active": manager.path.name}


@router.post("/presets/save")
async def create_preset(req: PresetCreateRequest):
    """把当前激活方案另存为新方案并切换过去。"""
    from mdcx.config.manager import manager
    name = req.name.strip()
    if not _PRESET_NAME_RE.match(name):
        return {"ok": False, "error": "方案名仅允许中文/字母/数字/空格/连字符（1-40字符）"}
    target = _preset_path(name)
    if target.exists():
        return {"ok": False, "error": f"方案 {name} 已存在"}
    try:
        Path(manager.path).read_bytes()  # 确保激活方案存在
        manager.path = target            # setter 会写 MARK_FILE
        manager.save()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "active": target.name}


@router.post("/presets/switch")
async def switch_preset(req: PresetSwitchRequest):
    from mdcx.config.manager import manager
    target = _preset_path(req.name.strip())
    if not target.is_file():
        return {"ok": False, "error": "方案不存在"}
    try:
        manager.path = target    # setter 写 MARK_FILE + 重载路径
        manager.load()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "active": target.name}


@router.post("/presets/delete")
async def delete_preset(req: PresetDeleteRequest):
    from mdcx.config.manager import manager
    name = req.name.strip()
    target = _preset_path(name)
    if not target.is_file():
        return {"ok": False, "error": "方案不存在"}
    if target.name == "config.json":
        return {"ok": False, "error": "默认方案不可删除"}
    if manager.path.name == target.name:
        # 切回默认再删除
        default = _preset_path("config.json")
        if default.is_file():
            manager.path = default
            manager.load()
    try:
        target.unlink()
    except OSError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True}


@router.get("/list")
async def list_configs():
    from mdcx.config.manager import manager

    try:
        items = manager.list_configs()
    except Exception:  # noqa: BLE001
        items = []
    return {"ok": True, "configs": items, "current": str(manager.path)}