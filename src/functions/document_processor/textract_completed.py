from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any):
    print(event["Records"])
