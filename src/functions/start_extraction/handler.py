from typing import Dict, Any

from src.main.composers.start_extraction_text_composer import StartExtractionTextComposer

def handler(event: Dict[str, Any], context: Any):
    compose = StartExtractionTextComposer.compose()
    compose(event["detail"]["object"]["key"])
