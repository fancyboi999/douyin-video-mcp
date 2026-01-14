"""ASR 提供方工厂"""

from typing import Optional

from .base import ASRProvider
from .dashscope_provider import DashscopeASRProvider
from .fish_provider import FishASRProvider
from ..config import (
    DEFAULT_ASR_PROVIDER,
    ENV_ASR_PROVIDER,
    ENV_DASHSCOPE_KEY,
    ENV_FISH_KEY,
    get_env,
)


def normalize_provider_name(name: Optional[str]) -> str:
    if not name:
        return ""
    return name.strip().lower()


def resolve_provider_name(explicit: Optional[str]) -> str:
    if explicit:
        return normalize_provider_name(explicit)
    env_value = get_env(ENV_ASR_PROVIDER, DEFAULT_ASR_PROVIDER)
    return normalize_provider_name(env_value)


def get_asr_provider(provider: Optional[str], model: Optional[str]) -> ASRProvider:
    provider_name = resolve_provider_name(provider)

    if provider_name in ("", "dashscope", "ali", "aliyun"):
        api_key = get_env(ENV_DASHSCOPE_KEY)
        if not api_key:
            raise ValueError("未设置环境变量 DASHSCOPE_API_KEY")
        return DashscopeASRProvider(api_key=api_key, model=model)

    if provider_name in ("fish", "fishaudio", "fish-audio"):
        api_key = get_env(ENV_FISH_KEY)
        if not api_key:
            raise ValueError("未设置环境变量 FISH_API_KEY")
        return FishASRProvider(api_key=api_key)

    raise ValueError(f"不支持的 ASR 提供方: {provider_name}")
