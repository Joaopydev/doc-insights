import fitz

from src.processing.application.ports.text_extractor import (
    TextExtractor as TextExtractorInterface
)


class TextExtractor(TextExtractorInterface):

    def extract(self, file_bytes: bytes):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""

        for page in doc:
            text += page.get_text()

        return text
