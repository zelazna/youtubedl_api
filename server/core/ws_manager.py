import json

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from server.core import Request, logger


class WsConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_direct_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
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


manager = WsConnectionManager()
