import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import cast

import ffmpeg
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import server.api.requests.schemas as schemas
from server.api.downloads import DownloadCreate, downloads
from server.api.shared import get_db
from server.core import Request, logger, manager, settings
from server.core.adapters import BaseAdapter
from server.core.models import State

from .crud import requests

requests_router = APIRouter(prefix="/requests")

ExtensionNeedFFMPEG = {"mp3"}


def convert_to_extension(file: str, extension: str) -> str:
    # TODO https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#generate-thumbnail-for-video
    logger.debug("converting %s to %s", file, extension)
    new_filename = f"{settings.STATIC_FOLDER}/{Path(file).stem}.{extension}"
    ffmpeg.input(file).output(new_filename).run(quiet=True, overwrite_output=True)
    return new_filename


async def broadcast_state(request: Request):
    request_dict = jsonable_encoder(request)
    request_dict["download"] = jsonable_encoder(request.download)
    await manager.broadcast(json.dumps(request_dict))


async def download_file(
    request: Request,
    db: Session,
    extension: str = "mp4",
):
    try:
        await broadcast_state(request)
        loop = asyncio.get_running_loop()
        executor = ThreadPoolExecutor()
        convert_to = None
        if extension in ExtensionNeedFFMPEG:
            extension, convert_to = "mp4", extension

        logger.debug("starting download of %s", request.url)
        request = requests.set_state(db, request, State.in_progress)
        await broadcast_state(request)
        adapter = cast(BaseAdapter, settings.VIDEO_ADAPTER_IMPL)
        file, thumbnail, name = await loop.run_in_executor(
            executor,
            adapter.download_video,
            request.url,
            settings.STATIC_FOLDER,
            extension,
        )
        logger.debug("download of %s finished", request.url)

        if convert_to:
            file = await loop.run_in_executor(
                executor, convert_to_extension, file, convert_to
            )
    except Exception as e:
        requests.set_state(db, request, State.in_error)
        await broadcast_state(request)
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
        # TODO find why session.flush discard current object
        request = requests.set_state(
            db, cast(Request, requests.get(db, request.id)), State.done
        )
        await broadcast_state(request)
        logger.debug("creating a download with name: %s", download.url)


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
    background_tasks.add_task(download_file, req, db, request.extension)
    return req
