"""抖音链接解析与下载"""

import json
import re
import tempfile
from pathlib import Path
from typing import Optional

import ffmpeg
import requests
from mcp.server.fastmcp import Context

from .config import HEADERS


class DouyinProcessor:
    """抖音视频处理器"""

    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def __del__(self):
        """清理临时目录"""
        import shutil

        if hasattr(self, "temp_dir") and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def parse_share_url(self, share_text: str) -> dict:
        """从分享文本中提取无水印视频链接"""
        urls = re.findall(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            share_text,
        )
        if not urls:
            raise ValueError("未找到有效的分享链接")

        share_url = urls[0]
        share_response = requests.get(share_url, headers=HEADERS)
        video_id = share_response.url.split("?")[0].strip("/").split("/")[-1]
        share_url = f"https://www.iesdouyin.com/share/video/{video_id}"

        response = requests.get(share_url, headers=HEADERS)
        response.raise_for_status()

        pattern = re.compile(
            pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
            flags=re.DOTALL,
        )
        find_res = pattern.search(response.text)

        if not find_res or not find_res.group(1):
            raise ValueError("从HTML中解析视频信息失败")

        json_data = json.loads(find_res.group(1).strip())
        video_page_key = "video_(id)/page"
        note_page_key = "note_(id)/page"

        if video_page_key in json_data["loaderData"]:
            original_video_info = json_data["loaderData"][video_page_key]["videoInfoRes"]
        elif note_page_key in json_data["loaderData"]:
            original_video_info = json_data["loaderData"][note_page_key]["videoInfoRes"]
        else:
            raise Exception("无法从JSON中解析视频或图集信息")

        data = original_video_info["item_list"][0]
        video_url = data["video"]["play_addr"]["url_list"][0].replace(
            "playwm", "play"
        )
        desc = data.get("desc", "").strip() or f"douyin_{video_id}"
        desc = re.sub(r"[\\/:*?\"<>|]", "_", desc)

        return {"url": video_url, "title": desc, "video_id": video_id}

    async def download_video(self, video_info: dict, ctx: Optional[Context]) -> Path:
        """异步下载视频到临时目录"""
        filename = f"{video_info['video_id']}.mp4"
        filepath = self.temp_dir / filename

        if ctx:
            ctx.info(f"正在下载视频: {video_info['title']}")

        response = requests.get(video_info["url"], headers=HEADERS, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with open(filepath, "wb") as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0 and ctx:
                        await ctx.report_progress(downloaded, total_size)

        if ctx:
            ctx.info(f"视频下载完成: {filepath}")

        return filepath

    def extract_audio(self, video_path: Path) -> Path:
        """从视频文件中提取音频"""
        audio_path = video_path.with_suffix(".mp3")

        try:
            (
                ffmpeg.input(str(video_path))
                .output(str(audio_path), acodec="libmp3lame", q=0)
                .run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            )
            return audio_path
        except Exception as exc:
            raise Exception(f"提取音频时出错: {str(exc)}")

    def cleanup_files(self, *file_paths: Path) -> None:
        """清理指定的文件"""
        for file_path in file_paths:
            if file_path and file_path.exists():
                file_path.unlink()
