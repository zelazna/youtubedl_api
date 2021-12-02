from typing import Any, Optional


class VideoNotFound(Exception):
    pass


VideoData = tuple[str, str, str]


class BaseAdapter:
    def on_progress_callback(self, stream: Any, chunk: bytes, bytes_remaining: int):
        raise NotImplementedError

    def on_complete_callback(self, stream: Any, file_path: Optional[str]):
        raise NotImplementedError

    def download_video(self, video: str, folder: str, file_extension: str) -> VideoData:
        raise NotImplementedError

    def download_playlist(self, url: str, folder: str) -> list[VideoData]:
        raise NotImplementedError


from .pytube_adapter import PytubeAdapter
