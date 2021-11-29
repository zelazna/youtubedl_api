from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from server.core import Base


class Download(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column("name", String)
    vanilla_url = Column("vanilla_url", String)
    thumbnail_url = Column("thumbnail_url", String)
    url = Column("url", String)
    download_request = relationship("DownloadRequest", back_populates="download")
