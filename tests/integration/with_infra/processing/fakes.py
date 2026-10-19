from src.processing.application.ports.text_extractor import TextExtractor


class FakeTextExtractor(TextExtractor):
    def __init__(self, job_id: str = "fake-textract-job-id"):
        self.job_id = job_id
        self.calls = []

    def start_extraction(self, storage_key: str, document_id: str) -> str:
        self.calls.append({"storage_key": storage_key, "document_id": document_id})
        return self.job_id

    def get_document_text(self, *args, **kwargs):
        raise NotImplementedError

    def _blocks_to_text(self, *args, **kwargs):
        raise NotImplementedError

    def _clean_line_texts(self, *args, **kwargs):
        raise NotImplementedError

    def _detect_boilerplate(self, *args, **kwargs):
        raise NotImplementedError

    def _is_short_token(self, *args, **kwargs):
        raise NotImplementedError

    def _normalize(self, *args, **kwargs):
        raise NotImplementedError
