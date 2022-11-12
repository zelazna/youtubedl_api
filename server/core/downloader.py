import asyncio
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable, cast

import ffmpeg

from server.core.adapters import BaseAdapter, VideoData
from server.core.settings import logger, settings

ExtensionNeedFFMPEG = {"mp3"}


def convert_to_extension(file: str, extension: str) -> str:
    # TODO https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#generate-thumbnail-for-video
    logger.debug("converting %s to %s", file, extension)
    new_filename = f"{settings.STATIC_FOLDER}/{Path(file).stem}.{extension}"
    ffmpeg.input(file).output(new_filename).run(quiet=True, overwrite_output=True)
    return new_filename


async def noop():
    ...


async def download_file(
    url: str,
    extension: str,
    progress_hook: Callable[..., Any] = noop,
) -> VideoData:
    loop, convert_to = asyncio.get_running_loop(), None

    if extension in ExtensionNeedFFMPEG:
        extension, convert_to = "mp4", extension

    logger.debug("starting download of %s", url)

    if progress_hook:
        await progress_hook()

    adapter = cast(BaseAdapter, settings.VIDEO_ADAPTER_IMPL)

    file, thumbnail, name = await loop.run_in_executor(
        None,
        adapter.download_video,
        url,
        settings.STATIC_FOLDER,
        extension,
    )
    logger.debug("download of %s finished", name)

    if convert_to:
        with ProcessPoolExecutor() as pool:
            file = await loop.run_in_executor(
                pool, convert_to_extension, file, convert_to
            )
    return file, thumbnail, name
