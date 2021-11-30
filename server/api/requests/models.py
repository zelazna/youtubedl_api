import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from server.core import Base


class LinkType(enum.Enum):
    video = "video"
    playlist = "playlist"


class State(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    in_error = "error"
    done = "done"


class Request(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column("type", Enum(LinkType))
    url = Column("url", String)
    state = Column("state", Enum(State), default=State.pending)
    download = relationship("Download", back_populates="request", uselist=False)
