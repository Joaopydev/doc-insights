import asyncio
from typing import Dict, Any

from src.main.composers.index_document_compose import IndexDocumentComposer


async def async_handler(event: Dict[str, Any], context: Any):
    compose = IndexDocumentComposer.compose()
    await compose(event["detail"]["object"]["key"])

def handler(event: Dict[str, Any], context: Any):
    asyncio.run(async_handler(event, context))
