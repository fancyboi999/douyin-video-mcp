"""Fish Audio ASR"""

from pathlib import Path
from typing import Optional

import requests

from .base import ASRProvider


class FishASRProvider(ASRProvider):
    name = "fish"
    requires_audio = True

    def __init__(self, api_key: str):
        self.api_key = api_key

    def transcribe(self, *, video_url: str, audio_path: Optional[Path]) -> str:
        if not audio_path:
            raise ValueError("Fish ASR 需要音频文件")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"ignore_timestamps": "true"}

        try:
            with open(audio_path, "rb") as audio_file:
                files = {"audio": audio_file}
                response = requests.post(
                    "https://api.fish.audio/v1/asr",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120,
                )
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            raise Exception(f"Fish ASR 请求失败: {str(exc)}")

        text = payload.get("text")
        if not text:
            raise Exception("Fish ASR 未返回文本内容")
        return text
