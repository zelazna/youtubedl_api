from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.api.dependencies import get_current_active_user, get_current_user_ws, get_db
from server.core.jobs import download
from server.core.ws_manager import manager
from server.crud.requests import request
from server.crud.users import user
from server.models.user import User
from server.schemas.requests import RequestCreate, RequestInDB

requests_router = APIRouter()


@requests_router.get("/", response_model=list[RequestInDB])
def get_requests(
    skip: int = 0,
    limit: int = 100,
    orderby: str = "id desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if user.is_superuser(current_user):
        requests = request.get_multi(db, skip=skip, limit=limit)
    else:
        requests = request.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit, order_by=orderby
        )
    return requests


@requests_router.post("/", status_code=status.HTTP_200_OK, response_model=RequestInDB)
def create_request(
    request_obj: RequestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        req = request.create_with_owner(
            db, obj_in=request_obj, owner_id=current_user.id
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Download already exists"
        )
    else:
        background_tasks.add_task(download, req, db, request_obj.extension)
        return req


@requests_router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if request_obj := request.get(db, request_id):
        if request_obj.owner_id != current_user.id:
            raise HTTPException(status_code=400, detail="Not enough permissions")
        if request_obj.download:
            Path.unlink(Path(request_obj.download.url), missing_ok=True)
            Path.unlink(Path(request_obj.download.thumbnail_url), missing_ok=True)
        return request.remove(db, id=request_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Download doesn't exists"
    )


@requests_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: User = Depends(get_current_user_ws),
):
    await manager.connect(websocket, current_user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, current_user.id)
