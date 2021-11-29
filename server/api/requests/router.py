from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import server.api.requests.models as models
import server.api.requests.schemas as schemas
from server.api.shared import get_db

requests_router = APIRouter(prefix="/requests")


@requests_router.get("/", response_model=list[schemas.DownloadRequestInDB])
def get_download_requests(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return db.query(models.DownloadRequest).offset(skip).limit(limit).all()


@requests_router.post(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.DownloadRequestInDB
)
def create_download_request(
    download_request: schemas.DownloadRequestCreate, db: Session = Depends(get_db)
):
    db_item = models.DownloadRequest(**download_request.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
