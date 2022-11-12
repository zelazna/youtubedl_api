from abc import ABC, abstractmethod
from typing import Any, Optional


class VideoNotFound(Exception):
    pass


VideoData = tuple[str, str, str]


class BaseAdapter(ABC):
    @abstractmethod
    def on_progress_callback(self, stream: Any, chunk: bytes, bytes_remaining: int):
        ...

    @abstractmethod
    def on_complete_callback(self, stream: Any, file_path: Optional[str]):
        ...

    @abstractmethod
    def download_video(self, video: str, folder: str, file_extension: str) -> VideoData:
        ...

    @abstractmethod
    def download_playlist(self, url: str, folder: str) -> list[VideoData]:
        ...


from .pytube_adapter import PytubeAdapter
