import json
from typing import Dict

import boto3

from src.shared.application.ports.message_publisher import MessagePublisher
from src.main.config.settings import settings


class SQSPublisher(MessagePublisher):

    def __init__(self):
        self.client = boto3.client("sqs")

    def send_message(self, message_body: Dict[str, any]) -> None:
        self.client.send_message(
            QueueUrl=settings.questions_queue,
            MessageBody=json.dumps(message_body),
        )
