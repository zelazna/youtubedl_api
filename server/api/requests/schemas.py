from pydantic import BaseModel

from server.api.shared import LinkType

from .models import DownloadState


# Shared properties
class DownloadRequestBase(BaseModel):
    url: str
    type: LinkType


# Properties to receive on item creation
class DownloadRequestCreate(DownloadRequestBase):
    ...


# Properties shared by models stored in DB
class DownloadRequestInDBBase(DownloadRequestBase):
    id: int
    url: str
    type: LinkType
    state: DownloadState

    class Config:
        orm_mode = True


# Properties to return to client
class DownloadRequest(DownloadRequestInDBBase):
    pass


# Properties properties stored in DB
class DownloadRequestInDB(DownloadRequestInDBBase):
    pass
