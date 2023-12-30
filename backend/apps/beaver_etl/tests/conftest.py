import pytest

from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture(scope="session")
def mongo_db_container() -> MongoDbContainer:
    with MongoDbContainer("mongo:7.0.5-rc0") as container:
        yield container


@pytest.fixture(scope="function")
def mongo_db(mongo_db_container: MongoDbContainer) -> MongoClient:
    mongo_client = mongo_db_container.get_connection_client()

    yield mongo_client

    for db_name in mongo_client.list_database_names():
        if db_name not in {"admin", "config", "local"}:
            mongo_client.drop_database(db_name)
