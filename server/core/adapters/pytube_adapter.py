import urllib.request
from pathlib import Path
from typing import Any, Optional, Union

from pytube import YouTube
from pytube.contrib.playlist import Playlist

from server.core.adapters import BaseAdapter, VideoData, VideoNotFound


class PytubeAdapter(BaseAdapter):
    def on_progress_callback(self, stream: Any, chunk: bytes, bytes_remaining: int):
        pass

    def on_complete_callback(self, stream: Any, file_path: Optional[str]):
        pass

    def download_video(self, video: Union[str, YouTube], folder: str) -> VideoData:
        yt = YouTube(video) if isinstance(video, str) else video
        yt.register_on_progress_callback(self.on_progress_callback)
        yt.register_on_complete_callback(self.on_complete_callback)

        if stream := yt.streams.filter(file_extension="mp4").first():
            video_file = stream.download(output_path=folder)
            video_name = Path(video_file).stem
            thumnnail_file, _ = urllib.request.urlretrieve(
                yt.thumbnail_url, f"{folder}/thumb_{video_name}.jpg"
            )
            return (video_file, thumnnail_file, video_name)
        raise VideoNotFound

    def download_playlist(self, url: str, folder: str) -> list[VideoData]:
        return [self.download_video(v, folder) for v in Playlist(url).videos]
