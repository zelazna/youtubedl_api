from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from server.core import Base


class Download(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column("name", String)
    vanilla_url = Column("vanilla_url", String)
    thumbnail_url = Column("thumbnail_url", String)
    url = Column("url", String)
    request_id = Column(Integer, ForeignKey("request.id"))
    request = relationship("Request", back_populates="download")
