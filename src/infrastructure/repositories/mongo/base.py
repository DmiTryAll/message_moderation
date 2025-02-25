from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection


@dataclass
class BaseMongoDBRepository(ABC):
    mongodb_client: AgnosticClient
    mongodb_db_name: str
    mongodb_collection_name: str

    @property
    def _collection(self) -> AgnosticCollection:
        return self.mongodb_client[self.mongodb_db_name][self.mongodb_collection_name]