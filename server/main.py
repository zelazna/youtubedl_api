from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.api.requests import requests_router
from server.api.users import user_router
from server.core.settings import settings
from server.core.ws_manager import manager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FIXME
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(requests_router)
app.include_router(user_router)
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
