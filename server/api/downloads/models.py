from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from server.api.shared import LinkType
from server.models import Base


class Download(Base):
    id = Column(Integer, primary_key=True, index=True)
    type = Column("type", Enum(LinkType))
    name = Column("name", String)
    vanilla_url = Column("vanilla_url", String)
    thumbnail_url = Column("thumbnail_url", String)
    url = Column("url", String)
    download_request = relationship("Item", back_populates="download")
