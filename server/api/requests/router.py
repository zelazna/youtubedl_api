from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

import server.api.requests.models as models
import server.api.requests.schemas as schemas
from server.api.downloads import DownloadCreate, downloads
from server.api.shared import get_db
from server.core import settings

from .crud import requests

requests_router = APIRouter(prefix="/requests")


def download_file(request: models.Request, db: Session):
    try:
        if adapter := settings.VIDEO_ADAPTER_IMPL:
            requests.set_in_progress(db, request)
            file, thumbnail, name = adapter.download_video(
                request.url, settings.STATIC_FOLDER
            )
            requests.set_done(db, request)
            download = DownloadCreate(
                request_id=request.id,
                name=name,
                vanilla_url=request.url,
                thumbnail_url=thumbnail,
                url=file,
            )
            downloads.create(db, obj_in=download)
        else:
            raise Exception("No Adapter Configured")
    except Exception:
        requests.set_in_error(db, request)
        raise


@requests_router.get("/", response_model=list[schemas.RequestInDB])
def get_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return requests.get_multi(db, skip=skip, limit=limit)


@requests_router.post(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.RequestInDB
)
def create_request(
    request: schemas.RequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    req = requests.create(db, obj_in=request)
    background_tasks.add_task(download_file, req, db)
    return req
