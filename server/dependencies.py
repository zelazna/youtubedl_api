import json
from functools import lru_cache

from server.config import Config, load_conf
from server.rabbitmq import RabbitMq


@lru_cache()
def get_config() -> Config:
    with open("config.json", "r", encoding="utf-8") as fp:
        return load_conf(json.load(fp))


@lru_cache()
def get_rmq() -> RabbitMq:
    return RabbitMq()
