import json
import boto3

from src.main.config.logger import logger
from src.shared.application.ports.event_publisher import EventPublisher
from src.shared.application.events.domain_event import DomainEvent


class EventBridgeClient(EventPublisher):

    def __init__(self) -> None:

        self.client = boto3.client("events")

    def publish(self, event: DomainEvent) -> None:
        response = self.client.put_events(
            Entries=[
                {
                    "Source": event.source,
                    "DetailType": event.detail_type,
                    "Detail": json.dumps(event.detail),
                    "EventBusName": "default",
                }
            ]
        )

        if response["FailedEntryCount"] > 0:
            logger.error("Failed to publish event: %s", response["Entries"])
            raise RuntimeError("Failed to publish event")
