import json
from dataclasses import dataclass
from typing import Any, Callable

import aio_pika
from aio_pika.message import IncomingMessage

from server.config import Config


class NotInitializedExchange(Exception):
    ...


@dataclass(init=False)
class RabbitMq:
    write_channel: aio_pika.Channel
    read_channel: aio_pika.Channel
    read_connection: aio_pika.Connection
    write_connection: aio_pika.Connection
    queue: aio_pika.Queue

    async def start(self, config: Config):
        self.read_connection = await aio_pika.connect_robust(config.amqp.host)
        self.write_connection = await aio_pika.connect_robust(config.amqp.host)
        self.read_channel = await self.read_connection.channel()
        self.write_channel = await self.write_connection.channel()
        await self.read_channel.set_qos(prefetch_count=100)
        self.queue = await self.read_channel.declare_queue(
            config.amqp.queue, auto_delete=True
        )

    async def consume(self, callback: Callable[[IncomingMessage], Any]):
        await self.queue.consume(callback)

    # TODO handle exchanges
    async def publish(self, data: dict[str, Any], routing_key: str):
        if self.write_channel.default_exchange:
            await self.write_channel.default_exchange.publish(
                aio_pika.Message(json.dumps(data).encode()), routing_key
            )
        else:
            raise NotInitializedExchange

    async def stop(self):
        await self.write_connection.close()
        await self.read_connection.close()
