from enum import StrEnum


class DocumentStatus(StrEnum):
    UPLOADING = "UPLOADING"

    EXTRACTING = "EXTRACTING"
    EXTRACTED = "EXTRACTED"

    INDEXING = "INDEXING"

    READY = "READY"

    FAILED = "FAILED"
