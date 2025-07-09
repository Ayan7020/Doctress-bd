from services.conversation.create_conversation_controller import Create_conversation_controller
from fastapi import APIRouter , Depends , Request
from middleware.isAuthenticated import is_authenticated
from core.database import get_db

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