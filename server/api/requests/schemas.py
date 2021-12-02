from typing import Optional

from pydantic import BaseModel

from server.api.downloads.schemas import Download
from server.core import LinkType, State


# Shared properties
class RequestBase(BaseModel):
    url: str
    type: LinkType


# Properties to receive on item creation
class RequestCreate(RequestBase):
    ...


# Properties shared by models stored in DB
class RequestInDBBase(RequestBase):
    id: int
    url: str
    type: LinkType
    state: State
    download: Optional[Download]

    class Config:
        orm_mode = True


# Properties to return to client
class Request(RequestInDBBase):
    pass


# Properties properties stored in DB
class RequestInDB(RequestInDBBase):
    pass
