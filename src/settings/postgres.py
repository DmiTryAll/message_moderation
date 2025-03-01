from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    driver: str = "asyncpg"
    system: str = "postgresql"
    name: str
    user: str
    password: str | None = None
    port: int
    host: str = "localhost"

    @property
    def url(self):
        return "{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}".format(
            dialect=self.system,
            driver=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )