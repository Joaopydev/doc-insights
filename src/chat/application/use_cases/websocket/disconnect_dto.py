from pydantic import BaseModel


class WebSocketDisconnectInput(BaseModel):
    connection_id: str
