from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.api.dependencies import get_current_active_user, get_db
from server.core.security import create_access_token
from server.core.settings import settings
from server.crud.users import user
from server.models.user import User
from server.schemas.token import Token
from server.schemas.users import User as UserSchema

user_router = APIRouter()


@user_router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user_ = user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user_:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active(user_):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@user_router.get("/me", response_model=UserSchema)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
