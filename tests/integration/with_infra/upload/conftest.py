import pytest
import boto3

from src.main.config.settings import settings

from src.upload.application.use_cases.create.create_document import CreateDocumentUseCase
from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.infrastructure.storage.s3 import S3Client
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


@pytest.fixture(scope="session", autouse=True)
def setup_upload_infrastructure():

    #Creating S3 local storage
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.aws_endpoint_url,
        region_name=settings.aws_default_region,
    )
    s3_client.create_bucket(Bucket=settings.bucket_name)

    #Creating DynamoDB local table
    dynamo = boto3.client(
        "dynamodb",
        endpoint_url=settings.aws_endpoint_url,
        region_name=settings.aws_default_region,
    )

    existing_tables = dynamo.list_tables()["TableNames"]

    if settings.document_table in existing_tables:
        dynamo.delete_table(TableName=settings.document_table)
        dynamo.get_waiter("table_not_exists").wait(
            TableName=settings.document_table
        )

    dynamo.create_table(
        TableName=settings.document_table,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    )

    yield


@pytest.fixture
def create_document_use_case() -> CreateDocumentUseCase:

    s3_client = S3Client()
    document_repository = DocumentRepository(DynamoDBClient())
    return CreateDocumentUseCase(
        document_repository=document_repository,
        storage_port=s3_client,
    )
