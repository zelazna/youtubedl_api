import logging
from logging.config import dictConfig
from typing import Any, Optional

from pydantic import BaseModel, BaseSettings, PostgresDsn, validator
from pydantic.networks import PostgresDsn

from server.core.adapters import BaseAdapter, PytubeAdapter


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "api"
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "api": {"handlers": ["default"], "level": LOG_LEVEL},
    }


class Settings(BaseSettings):
    LOGCONFIG: LogConfig = LogConfig()
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # TODO Convert it to Path type
    STATIC_FOLDER: str = "/files"

    VIDEO_ADAPTER: Optional[str]
    VIDEO_ADAPTER_IMPL: Optional[BaseAdapter] = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 50
    SECRET_KEY: str = "CHANGE_ME"

    FIRST_SUPERUSER: str = "root@root.com"
    FIRST_SUPERUSER_PASSWORD: str = "root"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", "localhost"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("VIDEO_ADAPTER_IMPL", pre=True)
    def instanciate_adapter(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        match values.get("VIDEO_ADAPTER"):
            case "pytube":
                return PytubeAdapter()
            case _:
                return PytubeAdapter()

    class Config:
        case_sensitive = True
        # arbitrary_types_allowed = True


settings = Settings()
logger = logging.getLogger("api")
dictConfig(settings.LOGCONFIG.dict())
