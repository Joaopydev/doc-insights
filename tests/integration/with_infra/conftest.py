#pylint: disable=import-outside-toplevel
import os
from dotenv import load_dotenv

import pytest
import boto3

current_dir = os.path.dirname(__file__)
env_test_path = os.path.abspath(os.path.join(current_dir, ".env.test"))

load_dotenv(dotenv_path=env_test_path, override=True)


@pytest.fixture(scope="session", autouse=True)
def setup_localstack_infrastructure():
    from src.main.config.settings import settings

    #Creating S3 local storage
    s3_client = boto3.client("s3")
    s3_client.create_bucket(Bucket=settings.bucket_name)

    #Creating DynamoDB local table
    dynamo = boto3.client("dynamodb")

    existing_tables = dynamo.list_tables()["TableNames"]

    if settings.document_table in existing_tables:
        dynamo.delete_table(TableName=settings.document_table)
        dynamo.get_waiter("table_not_exists").wait(
            TableName=settings.document_table
        )

    dynamo.create_table(
        TableName=settings.document_table,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "s3_key", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "storage-key-index",
                "KeySchema": [{"AttributeName": "s3_key", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            },
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    yield
