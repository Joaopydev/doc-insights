import boto3
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

from src.shared.application.ports.storage_port import StoragePort
from src.main.config.settings import settings



class S3Client(StoragePort):

    def __init__(self):
        self.s3_client = boto3.client("s3")

    def generate_presigned_url(
        self,
        file_key: str,
        content_type: str,
        expire_in: int
    ) -> str:
        return self.s3_client.generate_presigned_url(
            ClientMethod="put_object",
            ExpiresIn=expire_in,
            Params={
                "Bucket": settings.bucket_name,
                "Key": file_key,
                "ContentType": content_type
            }
        )


    def read_object_content(self, key):
        try:
            obj = self.s3_client.get_object(
                Bucket=settings.bucket_name,
                Key=key,
            )
            streaming_body: StreamingBody = obj["Body"]

            return streaming_body.read()
        except ClientError as e:
            raise RuntimeError(f"Failed to fetch object from s3: {e}") from e


    def put_object(
        self,
        key: str,
        body: any,
        content_type: str
    ) -> None:
        self.s3_client.put_object(
            Bucket=settings.bucket_name,
            Key=key,
            Body=body,
            ContentType=content_type,
        )
