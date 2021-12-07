from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import server.api.requests.schemas as schemas
from server.api.requests.jobs import download
from server.api.shared import get_db

from .crud import requests

requests_router = APIRouter(prefix="/requests")


@requests_router.get("/", response_model=list[schemas.RequestInDB])
def get_requests(
    skip: int = 0,
    limit: int = 100,
    orderby: str = "id desc",
    db: Session = Depends(get_db),
):
    return requests.get_multi(db, skip=skip, limit=limit, order_by=orderby)


@requests_router.post(
    "/", status_code=status.HTTP_200_OK, response_model=schemas.RequestInDB
)
def create_request(
    request: schemas.RequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        req = requests.create(db, obj_in=request)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Request already exists"
        )
    else:
        background_tasks.add_task(download, req, db, request.extension)
        return req


@requests_router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    if request := requests.get(db, request_id):
        if request.download:
            Path.unlink(Path(request.download.url))
            Path.unlink(Path(request.download.thumbnail_url))
        return requests.remove(db, id=request_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Request doesn't exists"
    )
