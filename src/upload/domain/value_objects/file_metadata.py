from dataclasses import dataclass


@dataclass(frozen=True)
class FileMetadata:
    filename: str
    content_type: str
    size: int

    def to_dict(self):
        return {
            "filename": self.filename,
            "content_type": self.content_type,
            "size": self.size
        }
