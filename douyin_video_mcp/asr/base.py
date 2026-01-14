"""ASR 提供方接口"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class ASRProvider(ABC):
    name: str = ""
    requires_audio: bool = False

    @abstractmethod
    def transcribe(self, *, video_url: str, audio_path: Optional[Path]) -> str:
        """转录语音为文本"""
        raise NotImplementedError
