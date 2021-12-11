from fastapi import APIRouter

from server.api.requests import requests_router
from server.api.users import user_router

api_router = APIRouter()
api_router.include_router(requests_router, prefix="/requests", tags=["requests"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
