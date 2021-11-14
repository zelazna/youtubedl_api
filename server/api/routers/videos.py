from dataclasses import asdict

from fastapi import APIRouter, Depends, status

from server.api.models.videos import DownloadRequest
from server.config import Config
from server.dependencies import get_config, get_rmq
from server.rabbitmq import RabbitMq

video_router = APIRouter(prefix="/videos")


@video_router.get("/")
async def list_():
    return [{"url": "https://coucou.fr"}]


@video_router.post("/", status_code=status.HTTP_201_CREATED)
async def download(
    video: DownloadRequest,
    rmq: RabbitMq = Depends(get_rmq),
    config: Config = Depends(get_config),
):
    await rmq.publish(asdict(video), config.amqp.routing_key)


@video_router.delete("/{id}")
async def delete_(
    id: str, rmq: RabbitMq = Depends(get_rmq), config: Config = Depends(get_config)
):
    ...
