import functools
from typing import cast

from sqlalchemy.orm import Session

from server.core.downloader import download_file
from server.core.settings import logger
from server.core.ws_manager import send_message
from server.crud.downloads import download as crud_download
from server.crud.requests import request
from server.models.request import Request, State
from server.schemas.downloads import DownloadCreate


async def next_state(db: Session, request_obj: Request, state: State):
    request.set_state(db, request_obj, state)
    await send_message(request_obj)


async def download(
    request_obj: Request,
    db: Session,
    extension: str = "mp4",
):
    try:
        await send_message(request_obj)
        file, thumbnail, name = await download_file(
            request_obj.url,
            extension,
            functools.partial(next_state, db, request_obj, State.in_progress),
        )
    except Exception as e:
        await next_state(db, request_obj, State.in_error)
        logger.error(e, exc_info=e)
    else:
        download = DownloadCreate(
            request_id=request_obj.id,
            name=name,
            vanilla_url=request_obj.url,
            thumbnail_url=thumbnail,
            url=file,
        )
        download_obj = crud_download.create(db, obj_in=download)
        logger.debug("creating a download with name: %s", download_obj.url)
        # Find why request lose his attrs because of flush
        await next_state(db, cast(Request, request.get(db, request_obj.id)), State.done)
