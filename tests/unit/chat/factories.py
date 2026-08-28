from typing import Optional, List

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.chat.domain.value_objects.message_type import MessageType

from src.shared.domain.entities.document import Document
from src.shared.domain.entities.chunk import DocumentChunk
from src.chat.domain.entities.conversation import Conversation
from src.chat.domain.entities.chat_message import ChatMessage

def create_document(
    user_id: str,
    filename: str,
    content_type: str,
    document_status: Optional[DocumentStatus] = None
) -> Document:
    document = Document.create(
        user_id=user_id,
        metadata={
            "filename": filename,
            "content_type": content_type,
        }
    )
    if document_status:
        document.status = document_status

    return document

def create_conversation(
    document_id: str,
    user_id: str
) -> Conversation:
    return Conversation.create(
        document_id=document_id,
        user_id=user_id,
    )

def create_message(
    conversation_id: str,
    content: str,
    message_type: MessageType,
) -> ChatMessage:
    return ChatMessage.create(
        conversation_id=conversation_id,
        content=content,
        message_type=message_type,
    )

def create_document_chunk(
    document_id: str,
    chunk_order: int,
    content: str,
    embedding: List[float]
) -> DocumentChunk:

    return DocumentChunk.create(
        document_id=document_id,
        chunk_order=chunk_order,
        content=content,
        embedding=embedding,
    )
