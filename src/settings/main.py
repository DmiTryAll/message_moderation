from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.mongodb import MongoDBConfig
from settings.postgres import PostgresConfig


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        env_nested_delimiter="__",
        extra="ignore"
    )

    mongodb: MongoDBConfig
    postgres: PostgresConfig

    telegram_token: str
    telegram_id: int

    path_to_progress_counter: Path = Path("progress_counter.txt")
    num_records_per_req: int = 50
    num_repetitions_for_report: int = 3
