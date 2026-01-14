"""阿里云百炼 ASR"""

import json
from http import HTTPStatus
from pathlib import Path
from typing import Optional
from urllib import request

import dashscope

from .base import ASRProvider
from ..config import DEFAULT_DASHSCOPE_MODEL


class DashscopeASRProvider(ASRProvider):
    name = "dashscope"
    requires_audio = False

    def __init__(self, api_key: str, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model or DEFAULT_DASHSCOPE_MODEL
        dashscope.api_key = api_key

    def transcribe(self, *, video_url: str, audio_path: Optional[Path]) -> str:
        try:
            task_response = dashscope.audio.asr.Transcription.async_call(
                model=self.model,
                file_urls=[video_url],
                language_hints=["zh", "en"],
            )

            transcription_response = dashscope.audio.asr.Transcription.wait(
                task=task_response.output.task_id
            )

            if transcription_response.status_code != HTTPStatus.OK:
                raise Exception(
                    f"转录失败: {transcription_response.output.message}"
                )

            for transcription in transcription_response.output["results"]:
                url = transcription["transcription_url"]
                result = json.loads(request.urlopen(url).read().decode("utf8"))
                if "transcripts" in result and len(result["transcripts"]) > 0:
                    return result["transcripts"][0]["text"]

            return "未识别到文本内容"
        except Exception as exc:
            raise Exception(f"提取文字时出错: {str(exc)}")
