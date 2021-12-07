from typing import Generator

from sqlalchemy.orm.session import Session

from server.core import SessionLocal


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
