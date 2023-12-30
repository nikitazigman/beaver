from abc import ABC, abstractmethod

from beaver_etl.schemas.loader import LoaderCodeSchema

from pymongo import MongoClient


class ILoader(ABC):
    @abstractmethod
    def load(self, code_schema: LoaderCodeSchema) -> None:
        ...


class MongoDBLoader(ILoader):
    def __init__(self, mongo_db: MongoClient, database: str, collection: str):
        self.client = mongo_db
        self.database = database
        self.collection = collection

    def load(self, code_schema: LoaderCodeSchema) -> None:
        self.client[self.database][self.collection].insert_one(
            code_schema.model_dump()
        )
