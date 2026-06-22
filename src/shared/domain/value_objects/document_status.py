from enum import StrEnum


class DocumentStatus(StrEnum):
    UPLOADING = "UPLOADING"
    EXTRACTING = "EXTRACTING"
    ANALYZING = "ANALYZING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
