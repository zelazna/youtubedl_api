import json

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from server.core.settings import logger
from server.models.request import Request


class WsConnectionManager:
    def __init__(self):
        self.active_connections: list[tuple[WebSocket, int]] = []

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections.append((websocket, client_id))

    def disconnect(self, websocket: WebSocket, client_id: int):
        self.active_connections.remove((websocket, client_id))

    async def send_direct_message(self, message: str, user_id: int):
        socket = next(
            ws for ws, client_id in self.active_connections if client_id == user_id
        )
        await socket.send_text(message)

    async def broadcast(self, message: str):
        for connection, _ in self.active_connections:
            await connection.send_text(message)


async def broadcast_state(request: Request):
    logger.debug("broadcasting %s %s", request.url, request.state)
    # TODO: find a way to serialize relationships
    await manager.broadcast(
        json.dumps(
            {
                **jsonable_encoder(request),
                "download": jsonable_encoder(request.download),
            }
        )
    )


async def send_message(request: Request):
    logger.debug("sending message to user %s", request.owner_id)
    # TODO: find a way to serialize relationships
    await manager.send_direct_message(
        json.dumps(
            {
                **jsonable_encoder(request),
                "download": jsonable_encoder(request.download),
            }
        ),
        request.owner_id,
    )


manager = WsConnectionManager()
