from typing import Dict, Any

from src.main.composers.process_document_composer import ProcessDocumentComposer

def handler(event: Dict[str, Any], context: Any):
    try:
        compose = ProcessDocumentComposer.compose()
        compose(event["detail"]["object"]["key"])
    except Exception as e:
        print("Error: ", e)
