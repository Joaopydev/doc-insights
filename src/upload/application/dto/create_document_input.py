from dataclasses import dataclass

from src.upload.domain.value_objects.file_metadata import FileMetadata


@dataclass(frozen=True)
class CreateDocumentInput:

    user_id: str
    metadata: FileMetadata
