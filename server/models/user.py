from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from server.db.base_class import Base
from server.models.request import Request


class User(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    full_name: str = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)
    request: Request = relationship("Request", back_populates="owner")
