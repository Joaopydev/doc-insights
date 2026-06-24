from datetime import datetime, UTC
from dataclasses import dataclass
from uuid import uuid4

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.shared.domain.value_objects.file_metadata import FileMetadata
from src.shared.domain.value_objects.s3_key import S3Key
from src.shared.domain.value_objects.extracted_text_key import ExtractedTextKey


@dataclass
class Document:
    id: str
    user_id: str

    s3_key: S3Key
    metadata: FileMetadata | None
    status: DocumentStatus
    extracted_text_key: ExtractedTextKey

    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: str,
        metadata: dict
    ) -> "Document":

        now = datetime.now(UTC)
        document_id = str(uuid4())
        file_metadata = FileMetadata(**metadata)

        s3_key = S3Key(
            f"users/{user_id}/documents/{document_id}/raw/{file_metadata.filename}"
        )
        extracted_text_key = ExtractedTextKey(
            f"users/{user_id}/documents/{document_id}/extracted/text.txt"
        )

        return cls(
            id=document_id,
            user_id=user_id,
            s3_key=s3_key,
            extracted_text_key=extracted_text_key,
            metadata=file_metadata,
            status=DocumentStatus.UPLOADING,
            created_at=now,
            updated_at=now
        )

    @classmethod
    def restore(
        cls,
        document_id: str,
        user_id: str,
        s3_key: str,
        extracted_text_key: str,
        metadata: dict,
        status: str,
        created_at: str,
        updated_at: str,
    ):
        file_metadata = FileMetadata(**metadata)
        s3_key = S3Key(s3_key)

        return cls(
            id=document_id,
            user_id=user_id,
            metadata=file_metadata,
            s3_key=s3_key,
            extracted_text_key=extracted_text_key,
            status=DocumentStatus(status),
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(updated_at)
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "s3_key": self.s3_key.get_value(),
            "extracted_text_key": self.extracted_text_key.get_value(),
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
