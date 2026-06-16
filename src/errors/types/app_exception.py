class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        name: str,
        message: str
    ):
        self.status_code = status_code
        self.name = name
        self.message = message
