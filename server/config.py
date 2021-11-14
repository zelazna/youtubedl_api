import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

import boto3

if TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client


@dataclass
class Amqp:
    host: str
    queue: str
    routing_key: str


@dataclass
class Bucket:
    name: str
    ak: str
    sk: str
    client: "S3Client" = field(init=False)
    region: str = "eu-west-2"
    endpoint: Optional[str] = None
    use_ssl: Optional[bool] = True

    def __post_init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.ak,
            aws_secret_access_key=self.sk,
            endpoint_url=self.endpoint,
            region_name=self.region,
            use_ssl=self.use_ssl,
        )


@dataclass
class Config:
    amqp: Amqp
    bucket: Bucket


def load_conf(params: dict[str, Any]) -> Config:
    amqp = Amqp(**params.pop("amqp"))
    bucket = Bucket(**params.pop("bucket"))
    return Config(**params, bucket=bucket, amqp=amqp)
