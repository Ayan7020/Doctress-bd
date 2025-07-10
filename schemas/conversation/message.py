
from pydantic import BaseModel

class MessageModel(BaseModel):
    query: str
    conversation_id: int
    session_id: str