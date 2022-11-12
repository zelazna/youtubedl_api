from typing import Generator, Optional

from fastapi import Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from server.core.security import ALGORITHM
from server.core.settings import settings
from server.crud.users import user
from server.db.session import SessionLocal
from server.models.user import User
from server.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_obj = user.get(db, id=token_data.sub)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj


async def get_current_user_ws(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    token: Optional[str] = Query(None),
) -> Optional[User]:
    token_data, user_obj = None, None
    try:
        payload = jwt.decode(token or "", settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    if token_data:
        user_obj = user.get(db, id=token_data.sub)
        if not user_obj:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return user_obj


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
