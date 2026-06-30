import boto3

from src.processing.application.ports.text_extractor import (
    TextExtractor as TextExtractorInterface
)
from src.main.config.settings import settings


class TextExtractor(TextExtractorInterface):

    def __init__(self):
        self.textract = boto3.client("textract")

    def start_extraction(self, storage_key: str, document_id: str) -> str:
        response = self.textract.start_document_text_detection(
            DocumentLocation={
                "S3Object": {
                    "Bucket": settings.bucket_name,
                    "Name": storage_key,
                }
            },
            NotificationChannel={
                "SNSTopicArn": settings.textract_topic_arn,
                "RoleArn": settings.textract_role_arn,
            },
            JobTag=document_id,
        )

        return response["JobId"]
