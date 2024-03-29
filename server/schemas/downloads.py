from datetime import datetime

from pydantic import BaseModel


# Shared properties
class DownloadBase(BaseModel):
    name: str
    vanilla_url: str
    thumbnail_url: str
    url: str


class DownloadCreate(DownloadBase):
    request_id: int


# Properties shared by models stored in DB
class DownloadInDBBase(DownloadCreate):
    id: int
    request_id: int
    created_at: datetime
    url: str
    name: str

    class Config:
        orm_mode = True


# Properties to return to client
class Download(DownloadInDBBase):
    pass


# Properties properties stored in DB
class DownloadInDB(DownloadInDBBase):
    ...
