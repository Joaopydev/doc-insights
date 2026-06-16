import json


class HTTPResponse:
    def __init__(self, status_code: int, body: dict = None):
        self.status_code = status_code
        self.body = body or {}
        self.headers = {
            "Content-Type": "application/json"
        }

    def to_dict(self):
        return {
            "statusCode": self.status_code,
            "body": json.dumps(self.body),
            "headers": self.headers,
        }
