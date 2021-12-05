from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.api.shared import get_db

from .crud import downloads
from .schemas import DownloadInDB

downloads_router = APIRouter(prefix="/downloads")


@downloads_router.get("/", response_model=list[DownloadInDB])
def get_downloads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return downloads.get_multi(db, skip=skip, limit=limit)
