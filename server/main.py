from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.api.routers.videos import video_router
from server.dependencies import get_config, get_rmq

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FIXME
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(video_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def on_app_start():
    await get_rmq().start(get_config())  # TODO: Refacto


@app.on_event("shutdown")
async def on_app_shutdown():
    await get_rmq().stop()
