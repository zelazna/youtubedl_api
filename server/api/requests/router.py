import subprocess
from pathlib import Path
from typing import cast

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

import server.api.requests.schemas as schemas
from server.api.downloads import DownloadCreate, downloads
from server.api.shared import get_db
from server.core import Request, logger, settings
from server.core.adapters import BaseAdapter

from .crud import requests

requests_router = APIRouter(prefix="/requests")

FormatNeedFFMPEG = {"mp3"}


def convert_to_format(file: str, format: str):
    new_filename = f"{Path(file).stem}.{format}"
    subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            new_filename,
        ]
    ).wait()
    return new_filename


def download_file(request: Request, db: Session, format: str = "mp4"):
    try:
        convert_to = None
        if format in FormatNeedFFMPEG:
            convert_to = format
            format = "mp4"

        logger.debug("starting download of %s", request.url)
        request = requests.set_in_progress(db, request)
        adapter = cast(BaseAdapter, settings.VIDEO_ADAPTER_IMPL)
        file, thumbnail, name = adapter.download_video(
            request.url, settings.STATIC_FOLDER, format
        )
        logger.debug("download of %s finished", request.url)

        if convert_to:
            file = convert_to_format(file, convert_to)

        request = requests.set_done(db, request)
    except Exception as e:
        requests.set_in_error(db, request)
        logger.error(e)
    else:
        download = DownloadCreate(
            request_id=request.id,
            name=name,
            vanilla_url=request.url,
            thumbnail_url=thumbnail,
            url=file,
        )
        download = downloads.create(db, obj_in=download)
        logger.debug("creating a download with name: %s", download.file)


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
    req = requests.create(db, obj_in=request)
    background_tasks.add_task(download_file, req, db)
    return req
