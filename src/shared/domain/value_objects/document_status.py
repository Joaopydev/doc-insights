from enum import StrEnum


class DocumentStatus(StrEnum):
    UPLOADING = "UPLOADING"
    EXTRACTING = "EXTRACTING"
    EXTRACTED = "EXTRACTED"
    ANALYZING = "ANALYZING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
