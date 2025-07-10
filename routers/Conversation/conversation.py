from services.conversation.create_conversation_controller import Create_conversation_controller
from services.conversation.create_message import create_message_controller
from fastapi import APIRouter , Depends , Request
from middleware.isAuthenticated import is_authenticated
from core.database import get_db
from schemas.conversation.message import MessageModel

router = APIRouter(
    dependencies=[Depends(is_authenticated)]
)


@router.post("/create-conversation")
async def Create_conversation(req: Request,session_name: str,db = Depends(get_db)):
    """
    It will create new  Conversation  and session id (authenticated route)
        Args:
            session_name: str
    """
    return await Create_conversation_controller(req,session_name,db)

@router.post("/chat/stream")
async def stream_chat(req: Request,data: MessageModel,db = Depends(get_db)):
    """
    Stream Chat Response from LLM with Memory + Database Logging

    This endpoint receives a user query as part of a conversation session,
    streams the LLM response token-by-token in real time,
    updates LangChain's Redis memory for the session,
    and saves the full message history into PostgreSQL.

    - **Request Body**: `MessageModel`
        - `query`: The user’s input/question.
        - `session_id`: A unique session identifier.
        - `conversation_id`: The DB conversation reference.
    - **Returns**: A `StreamingResponse` of the LLM-generated answer.
    """
    return await create_message_controller(req,data,db)