import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime


class LinkType(enum.Enum):
    video = "video"
    playlist = "playlist"


class State(enum.Enum):
    pending = "pending"
    in_progress = "in progress"
    in_error = "error"
    done = "done"


@as_declarative()
class Base:
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Download(Base):
    name = Column("name", String)
    vanilla_url = Column("vanilla_url", String)
    thumbnail_url = Column("thumbnail_url", String)
    url = Column("url", String)
    request_id = Column(Integer, ForeignKey("request.id", ondelete="CASCADE"))
    request = relationship("Request", back_populates="download")


class Request(Base):
    type = Column("type", Enum(LinkType))
    url = Column("url", String, unique=True)
    state = Column("state", Enum(State), default=State.pending)
    extension = Column("extension", String)
    download = relationship(
        "Download", back_populates="request", uselist=False, cascade="all, delete"
    )
