import json
import traceback
from typing import Dict, Any

from src.main.composers.textract_completed_composer import TextractCompletedComposer


def handler(event: Dict[str, Any], context: Any):
    try:
        message = json.loads(event["Records"][0]["Sns"]["Message"])
        job_id = message["JobId"]
        compose = TextractCompletedComposer.compose()
        compose(job_id)
    except Exception:
        traceback.print_exc()
        raise
