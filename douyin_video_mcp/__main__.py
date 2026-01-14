#!/usr/bin/env python3
"""
抖音MCP服务器入口点
"""

import argparse

from .config import (
    DEFAULT_MCP_HOST,
    DEFAULT_MCP_PATH,
    DEFAULT_MCP_PORT,
    DEFAULT_MCP_TRANSPORT,
    ENV_MCP_HOST,
    ENV_MCP_PATH,
    ENV_MCP_PORT,
    ENV_MCP_TRANSPORT,
    get_env,
)
from .server import main as server_main


def parse_args() -> argparse.Namespace:
    default_transport = get_env(ENV_MCP_TRANSPORT, DEFAULT_MCP_TRANSPORT)
    default_host = get_env(ENV_MCP_HOST, DEFAULT_MCP_HOST)
    default_path = get_env(ENV_MCP_PATH, DEFAULT_MCP_PATH)
    default_port = int(get_env(ENV_MCP_PORT, str(DEFAULT_MCP_PORT)))

    parser = argparse.ArgumentParser(description="Douyin Video MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "http", "sse"],
        default=default_transport,
        help="MCP 传输方式（默认读取 MCP_TRANSPORT）",
    )
    parser.add_argument(
        "--host",
        default=default_host,
        help="HTTP/SSE 监听地址（默认读取 MCP_HOST）",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=default_port,
        help="HTTP/SSE 端口（默认读取 MCP_PORT）",
    )
    parser.add_argument(
        "--path",
        default=default_path,
        help="HTTP/SSE 路径（默认读取 MCP_PATH）",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server_main(
        transport=args.transport,
        host=args.host,
        port=args.port,
        path=args.path,
    )


if __name__ == "__main__":
    main()
