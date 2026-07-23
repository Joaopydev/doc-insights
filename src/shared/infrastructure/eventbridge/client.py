import json
import boto3

from src.shared.application.ports.event_publisher import EventPublisher
from src.shared.application.events.domain_event import DomainEvent


class EventBridgeClient(EventPublisher):

    def __init__(self) -> None:

        self.client = boto3.client("events")

    def publish(self, event: DomainEvent) -> None:
        self.client.put_events(
            Entries=[
                {
                    "Source": event.source,
                    "DetailType": event.detail_type,
                    "Detail": json.dumps(event.detail),
                    "EventBusName": "default",
                }
            ]
        )
