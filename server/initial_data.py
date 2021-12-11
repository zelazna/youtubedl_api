from server.core.settings import logger
from server.db.init_db import init_db
from server.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
