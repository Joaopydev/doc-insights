from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedTextKey:
    value: str

    def get_value(self):
        return self.value
