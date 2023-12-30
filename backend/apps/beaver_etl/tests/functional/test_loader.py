import pytest

from beaver_etl.loaders.mongodb_loader import MongoDBLoader
from beaver_etl.schemas.loader import LoaderCodeSchema
from pymongo import MongoClient


@pytest.mark.parametrize(
    "loader_schema",
    (
        LoaderCodeSchema(
            source_code="test_code",
            language="python",
            link_to_task="test_link_to_task",
            title="test_title",
            readme="test_readme",
            types=["test_type1", "test_type2"],
            hash="test_hash",
        ),
    ),
)
def test_loader(
    mongo_db: MongoClient,
    loader_schema: LoaderCodeSchema,
):
    expected_document = loader_schema.model_dump()

    loader = MongoDBLoader(mongo_db, "test_db", "test_collection")
    loader.load(loader_schema)

    loaded_object = mongo_db["test_db"]["test_collection"].find_one(
        filter={"source_code": "test_code"}
    )
    assert loaded_object is not None

    loaded_object.pop("_id")
    assert loaded_object == expected_document
