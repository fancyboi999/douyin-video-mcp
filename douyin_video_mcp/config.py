"""共享配置与环境变量"""

import os
from typing import Optional

# 请求头，模拟移动端访问
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )
}

# 默认 ASR 配置
DEFAULT_ASR_PROVIDER = "dashscope"
DEFAULT_DASHSCOPE_MODEL = "paraformer-v2"

# 默认 MCP 运行配置
DEFAULT_MCP_TRANSPORT = "stdio"
DEFAULT_MCP_HOST = "127.0.0.1"
DEFAULT_MCP_PORT = 8000
DEFAULT_MCP_PATH = "/mcp/"

# 环境变量
ENV_ASR_PROVIDER = "ASR_PROVIDER"
ENV_DASHSCOPE_KEY = "DASHSCOPE_API_KEY"
ENV_FISH_KEY = "FISH_API_KEY"
ENV_MCP_TRANSPORT = "MCP_TRANSPORT"
ENV_MCP_HOST = "MCP_HOST"
ENV_MCP_PORT = "MCP_PORT"
ENV_MCP_PATH = "MCP_PATH"


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value
