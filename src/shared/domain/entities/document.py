from datetime import datetime, UTC
from dataclasses import dataclass
from uuid import uuid4

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.shared.domain.value_objects.file_metadata import FileMetadata
from src.shared.domain.value_objects.s3_key import S3Key


@dataclass
class Document:
    id: str
    user_id: str

    s3_key: S3Key
    metadata: FileMetadata | None
    status: DocumentStatus

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
            f"users/{user_id}/documents/{document_id}/{file_metadata.filename}"
        )

        return cls(
            id=document_id,
            user_id=user_id,
            s3_key=s3_key,
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
        metadata: dict,
        status: DocumentStatus,
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
            status=status,
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(updated_at)
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "s3_key": self.s3_key.get_value(),
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
