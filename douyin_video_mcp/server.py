#!/usr/bin/env python3
"""
抖音无水印视频下载并提取文本的 MCP 服务器

该服务器提供以下功能：
1. 解析抖音分享链接获取无水印视频链接
2. 下载视频并提取音频
3. 从音频中提取文本内容
4. 自动清理中间文件
"""

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP, Context

from .asr import get_asr_provider
from .config import ENV_ASR_PROVIDER, ENV_DASHSCOPE_KEY, ENV_FISH_KEY
from .douyin import DouyinProcessor


# 创建 MCP 服务器实例
mcp = FastMCP(
    "Douyin Video MCP Server",
    dependencies=["requests", "ffmpeg-python", "tqdm", "dashscope"],
)


@mcp.tool()
def get_douyin_download_link(share_link: str) -> str:
    """
    获取抖音视频的无水印下载链接

    参数:
    - share_link: 抖音分享链接或包含链接的文本

    返回:
    - 包含下载链接和视频信息的JSON字符串
    """
    try:
        processor = DouyinProcessor()
        video_info = processor.parse_share_url(share_link)

        return json.dumps(
            {
                "status": "success",
                "video_id": video_info["video_id"],
                "title": video_info["title"],
                "download_url": video_info["url"],
                "description": f"视频标题: {video_info['title']}",
                "usage_tip": "可以直接使用此链接下载无水印视频",
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as exc:
        return json.dumps(
            {"status": "error", "error": f"获取下载链接失败: {str(exc)}"},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
async def extract_douyin_text(
    share_link: str,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    ctx: Context = None,
) -> str:
    """
    从抖音分享链接提取视频中的文本内容

    参数:
    - share_link: 抖音分享链接或包含链接的文本
    - model: 语音识别模型（可选，默认使用paraformer-v2，仅 DashScope 生效）
    - provider: ASR 提供方（可选），默认读取环境变量 ASR_PROVIDER

    返回:
    - 提取的文本内容

    注意: 需要设置环境变量 DASHSCOPE_API_KEY 或 FISH_API_KEY
    """
    processor = DouyinProcessor()
    video_path = None
    audio_path = None

    try:
        if ctx:
            ctx.info("正在解析抖音分享链接...")
        video_info = processor.parse_share_url(share_link)

        asr_provider = get_asr_provider(provider, model)

        if ctx:
            ctx.info(f"正在使用 {asr_provider.name} 进行语音识别...")

        if asr_provider.requires_audio:
            if ctx:
                ctx.info("需要下载视频并提取音频...")
            video_path = await processor.download_video(video_info, ctx)
            audio_path = processor.extract_audio(video_path)

        text_content = asr_provider.transcribe(
            video_url=video_info["url"],
            audio_path=audio_path,
        )

        if ctx:
            ctx.info("文本提取完成!")
        return text_content

    except Exception as exc:
        if ctx:
            ctx.error(f"处理过程中出现错误: {str(exc)}")
        raise Exception(f"提取抖音视频文本失败: {str(exc)}")

    finally:
        processor.cleanup_files(
            *(path for path in (video_path, audio_path) if path is not None)
        )


@mcp.tool()
def parse_douyin_video_info(share_link: str) -> str:
    """
    解析抖音分享链接，获取视频基本信息

    参数:
    - share_link: 抖音分享链接

    返回:
    - 视频信息（JSON格式字符串）
    """
    try:
        processor = DouyinProcessor()
        video_info = processor.parse_share_url(share_link)

        return json.dumps(
            {
                "video_id": video_info["video_id"],
                "title": video_info["title"],
                "download_url": video_info["url"],
                "status": "success",
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as exc:
        return json.dumps(
            {"status": "error", "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.resource("douyin://video/{video_id}")
def get_video_info(video_id: str) -> str:
    """
    获取指定视频ID的详细信息

    参数:
    - video_id: 抖音视频ID

    返回:
    - 视频详细信息
    """
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}"
    try:
        processor = DouyinProcessor()
        video_info = processor.parse_share_url(share_url)
        return json.dumps(video_info, ensure_ascii=False, indent=2)
    except Exception as exc:
        return f"获取视频信息失败: {str(exc)}"


@mcp.prompt()
def douyin_text_extraction_guide() -> str:
    """抖音视频文本提取使用指南"""
    return f"""
# 抖音视频文本提取使用指南

## 功能说明
这个MCP服务器可以从抖音分享链接中提取视频的文本内容，以及获取无水印下载链接。

## 环境变量配置
请确保设置了以下环境变量：
- `{ENV_DASHSCOPE_KEY}`: 阿里云百炼API密钥（默认）
- `{ENV_FISH_KEY}`: Fish Audio API密钥（可选）
- `{ENV_ASR_PROVIDER}`: 默认 ASR 提供方（可选，例如 dashscope / fish）

## 使用步骤
1. 复制抖音视频的分享链接
2. 在 Claude Desktop 配置中设置环境变量
3. 使用相应的工具进行操作

## 工具说明
- `extract_douyin_text`: 完整的文本提取流程（支持多 ASR 提供方）
- `get_douyin_download_link`: 获取无水印视频下载链接（无需 API 密钥）
- `parse_douyin_video_info`: 仅解析视频基本信息
- `douyin://video/{{video_id}}`: 获取指定视频的详细信息

## Claude Desktop 配置示例
```json
{{
  "mcpServers": {{
    "douyin-video-mcp": {{
      "command": "uvx",
      "args": ["douyin-video-mcp"],
      "env": {{
        "{ENV_ASR_PROVIDER}": "fish",
        "{ENV_FISH_KEY}": "your-fish-api-key-here",
        "{ENV_DASHSCOPE_KEY}": "your-dashscope-api-key-here"
      }}
    }}
  }}
}}
```

## 注意事项
- 文本提取功能需要有效的 ASR API 密钥
- 获取下载链接无需 API 密钥
"""


def main(
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
    path: str = "/mcp/",
):
    """启动MCP服务器"""
    if transport in ("http", "sse"):
        mcp.run(transport=transport, host=host, port=port, path=path)
        return
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
