from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class MongoDBConfig(BaseSettings):
    model_config = ConfigDict(
        extra="ignore"
    )

    connection_uri: str
    database: str = Field(default="messages")
    messages_collection: str = Field(default="messages")