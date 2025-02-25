from pydantic import Field
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = Field(0, alias="database")
    user: str | None = None
    password: str | None = None

    @property
    def url(self):
        url = "redis://{}"
        if self.password and self.user:
            url = url.format("{username}:{password}@")
        else:
            url = url.format("")
        url += "{host}:{port}/{db}"
        return url.format(
            host=self.host,
            port=self.port,
            db=self.db,
            username=self.user,
            password=self.password,
        )