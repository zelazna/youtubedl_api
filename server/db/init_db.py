from sqlalchemy.orm import Session

from server.core.settings import settings
from server.crud.users import user
from server.db.base import Base  # noqa: F401
from server.db.session import engine
from server.schemas.users import UserCreate

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    user_obj = user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user_obj:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user_obj = user.create(db, obj_in=user_in)  # noqa: F841
