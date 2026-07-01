from typing import List, Dict
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

    def get_document_text(self, job_id: str) -> str:
        blocks = []
        next_token = None

        while True:
            kwargs = {"JobId": job_id}

            if next_token:
                kwargs["NextToken"] = next_token

            response = self.textract.get_document_text_detection(**kwargs)
            blocks.extend(response["Blocks"])

            next_token = response.get("NextToken")

            if not next_token:
                break

        return self._blocks_to_text(blocks)

    def _blocks_to_text(self, blocks: List[Dict]) -> str:
        lines = [block["Text"] for block in blocks if block["BlockType"] == "LINE"]
        return "\n".join(lines)
