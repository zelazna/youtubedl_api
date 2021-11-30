from functools import lru_cache
from typing import Generator

import boto3

from server.api.downloads.models import Download
from server.api.requests.models import Request
from server.core import SessionLocal, engine, settings
from server.core.base import Base

Base.metadata.create_all(bind=engine)


@lru_cache()
def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_AK,
        aws_secret_access_key=settings.AWS_SK,
        endpoint_url=settings.AWS_ENDPOINT,
        region_name=settings.AWS_REGION,
        use_ssl=settings.BOTO_USE_SSL,
    )


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
