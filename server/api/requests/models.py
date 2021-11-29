import enum

from sqlalchemy import Column, Enum, Integer, String

from server.api.shared import LinkType
from server.core import Base

# from sqlalchemy.orm import relationship


class DownloadState(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    error = "error"
    done = "done"


class DownloadRequest(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column("type", Enum(LinkType))
    url = Column("url", String)
    state = Column("state", Enum(DownloadState), default=DownloadState.pending)
    # download = relationship("Download", back_populates="download_request")
