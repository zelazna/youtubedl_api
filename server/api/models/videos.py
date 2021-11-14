import enum
from typing import Optional

from pydantic.dataclasses import dataclass


class LinkType(str, enum.Enum):
    video = "video"
    playlist = "playlist"


class DownloadState(str, enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    error = "error"
    done = "done"


@dataclass
class Download:
    id: Optional[str]
    type: LinkType
    path: Optional[str]
    name: str
    state: DownloadState = DownloadState.pending


@dataclass
class DownloadRequest:
    url: str
    type: LinkType = LinkType.video
