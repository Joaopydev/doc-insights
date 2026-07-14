from typing import List, Dict
import boto3

from src.processing.application.ports.text_extractor import (
    TextExtractor as TextExtractorInterface
)
from src.main.config.settings import settings

LAYOUT_BLOCKS_TO_SKIP = {"LAYOUT_HEADER", "LAYOUT_FOOTER", "LAYOUT_PAGE_NUMBER"}
REPETITION_THRESHOLD = 0.4
MAX_WORDS_FOR_BOILERPLATE_CHECK = 12


class TextExtractor(TextExtractorInterface):

    def __init__(self):
        self.textract = boto3.client("textract")

    def start_extraction(self, storage_key: str, document_id: str) -> str:
        response = self.textract.start_document_analysis(
            DocumentLocation={
                "S3Object": {
                    "Bucket": settings.bucket_name,
                    "Name": storage_key,
                }
            },
            FeatureTypes=[
                "LAYOUT"
            ],
            NotificationChannel={
                "SNSTopicArn": settings.textract_topic_arn,
                "RoleArn": settings.textract_role_arn,
            },
            JobTag=document_id,
        )

        return response["JobId"]

    def get_document_text(self, job_id: str) -> str:
        blocks = []
        next_token = None

        while True:
            kwargs = {"JobId": job_id}

            if next_token:
                kwargs["NextToken"] = next_token

            response = self.textract.get_document_analysis(**kwargs)
            blocks.extend(response["Blocks"])

            next_token = response.get("NextToken")

            if not next_token:
                break

        return self._blocks_to_text(blocks)

    def _blocks_to_text(self, blocks: List[Dict]) -> str:
        block_by_id = {b["Id"]: b for b in blocks}
        total_pages = max((b.get("Page", 1) for b in blocks), default=1)

        page_paragraphs: list[tuple[int, str]] = []

        for block in blocks:
            if not block["BlockType"].startswith("LAYOUT_"):
                continue
            if block["BlockType"] in LAYOUT_BLOCKS_TO_SKIP:
                continue

            child_ids = [
                cid
                for rel in block.get("Relationships", [])
                if rel["Type"] == "CHILD"
                for cid in rel["Ids"]
            ]
            line_texts = [
                block_by_id[cid]["Text"]
                for cid in child_ids
                if cid in block_by_id and block_by_id[cid]["BlockType"] == "LINE"
            ]
            line_texts = self._clean_line_texts(line_texts)
            paragraph = " ".join(line_texts).strip()

            if paragraph and not self._is_short_token(paragraph):
                page_paragraphs.append((block.get("Page", 1), paragraph))

        boilerplate = self._detect_boilerplate(page_paragraphs, total_pages)

        result = [
            paragraph
            for _, paragraph in page_paragraphs
            if self._normalize(paragraph) not in boilerplate
        ]

        return "\n\n".join(result)

    def _clean_line_texts(self, line_texts: list[str]) -> list[str]:
        return [t for t in line_texts if not self._is_short_token(t)]

    def _normalize(self, text: str) -> str:
        return " ".join(text.strip().lower().split())

    def _is_short_token(self, text: str) -> bool:
        normalized = text.strip()
        return len(normalized) <= 3 and normalized.isalpha()

    def _detect_boilerplate(
        self, page_paragraphs: list[tuple[int, str]], total_pages: int
    ) -> set[str]:
        pages_by_norm: dict[str, set[int]] = {}

        for page_num, paragraph in page_paragraphs:
            norm = self._normalize(paragraph)
            if len(norm.split()) <= MAX_WORDS_FOR_BOILERPLATE_CHECK:
                pages_by_norm.setdefault(norm, set()).add(page_num)

        return {
            norm
            for norm, pages_seen in pages_by_norm.items()
            if len(pages_seen) / total_pages >= REPETITION_THRESHOLD
        }
