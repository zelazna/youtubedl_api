from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.api import api_router
from server.core.settings import settings

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.mount("/files", StaticFiles(directory=settings.STATIC_FOLDER), name="files")
