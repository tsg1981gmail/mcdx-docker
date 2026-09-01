"""配置 API：读写 /data/config.json（mdcx ConfigManager 四步法 + 脱敏）。"""
from __future__ import annotations

from fastapi import APIRouter

from ..settings import settings

router = APIRouter()


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


@router.get("/list")
async def list_configs():
    from mdcx.config.manager import manager

    try:
        items = manager.list_configs()
    except Exception:  # noqa: BLE001
        items = []
    return {"ok": True, "configs": items, "current": str(manager.path)}