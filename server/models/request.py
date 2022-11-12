import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import Enum, Integer, String

from server.db.base_class import Base


class LinkType(enum.Enum):
    video = "video"
    playlist = "playlist"


class State(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    in_error = "error"
    done = "done"


class Request(Base):
    type = Column("type", Enum(LinkType))
    url: str = Column("url", String)
    state = Column("state", Enum(State), default=State.pending)
    extension = Column("extension", String)
    download = relationship(
        "Download", back_populates="request", uselist=False, cascade="all, delete"
    )
    owner = relationship("User", back_populates="request")
    owner_id: int = Column(Integer, ForeignKey("user.id"))

    __table_args__ = (UniqueConstraint("url", "extension"),)
