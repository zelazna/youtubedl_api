from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from server.db.base_class import Base


class Download(Base):
    name = Column("name", String)
    vanilla_url = Column("vanilla_url", String)
    thumbnail_url = Column("thumbnail_url", String)
    url = Column("url", String)
    request_id = Column(Integer, ForeignKey("request.id", ondelete="CASCADE"))
    request = relationship("Request", back_populates="download")
