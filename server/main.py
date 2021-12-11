from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from server.api import api_router
from server.core.settings import settings
from server.core.ws_manager import manager

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.mount("/files", StaticFiles(directory=settings.STATIC_FOLDER), name="files")


# Websocket bugged in APIrouter: https://github.com/tiangolo/fastapi/issues/98
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
