from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.mongodb import MongoDBConfig
from settings.redis import RedisConfig


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        env_nested_delimiter="__",
        extra="ignore"
    )

    mongodb: MongoDBConfig
    redis: RedisConfig

    telegram_token: str
    telegram_id: int

    num_records_per_req: int = 50
    num_repetitions_for_report: int = 2
