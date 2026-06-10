import boto3

from src.shared.application.ports.storage_port import StoragePort
from src.shared.settings.enviroment import settings


class S3Client(StoragePort):

    def __init__(self):
        self.bucket_name = settings.bucket_name
        self.s3_client = boto3.client("s3")

    def get_presigned_url(
        self,
        document_key: str,
        content_type: str,
        expire_in: int
    ) -> str:
        return self.s3_client.generate_presigned_url(
            ClientMethod="put_object",
            ExpiresIn=expire_in,
            Params={
                "Bucket": self.bucket_name,
                "Key": document_key,
                "ContentType": content_type
            }
        )
