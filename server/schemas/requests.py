from typing import Optional

from pydantic import BaseModel

from server.models.request import LinkType, State
from server.schemas.downloads import DownloadInDBBase


# Shared properties
class RequestBase(BaseModel):
    url: str
    type: LinkType
    extension: str


# Properties to receive on item creation
class RequestCreate(RequestBase):
    ...


# Properties shared by models stored in DB
class RequestInDBBase(RequestBase):
    id: int
    state: State
    download: Optional[DownloadInDBBase]

    class Config:
        orm_mode = True


# Properties to return to client
class Request(RequestInDBBase):
    pass


# Properties properties stored in DB
class RequestInDB(RequestInDBBase):
    pass
