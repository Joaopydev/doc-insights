from pydantic import BaseModel


class WebSocketConnectInput(BaseModel):
    user_id: str
    connection_id: str
