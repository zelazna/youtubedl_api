from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator
from pydantic.networks import PostgresDsn

# from server.core.adapters import BaseAdapter


class Settings(BaseSettings):
    BUCKET_NAME: str
    AWS_REGION: str = "eu-west-2"
    AWS_AK: str
    AWS_SK: str
    AWS_ENDPOINT: Optional[str]
    BOTO_USE_SSL: Optional[bool] = True

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    STATIC_FOLDER: str = "/static"
    # VIDEO_ADAPTER: BaseAdapter

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

    class Config:
        case_sensitive = True


settings = Settings()
