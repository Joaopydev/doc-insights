from dataclasses import dataclass


@dataclass(frozen=True)
class S3Key:
    value: str

    def get_value(self):
        return self.value
