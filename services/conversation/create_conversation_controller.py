from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from fastapi import Depends , Request , HTTPException
from models.conversation import Conversation
import uuid

async def Create_conversation_controller(req: Request,session_name: str,db: AsyncSession):
    """Controller for creating Conversation"""
    try:
        User = req.state.user
        
        if not User:
            raise HTTPException("Unauthorized access!")
        
        if not session_name:
            raise HTTPException("Session name should be present")
        
        user_id = User.id
        
        UniquesessionId = str(uuid.uuid4())
        new_conversation = Conversation(
            user_id=user_id,
            session_id=UniquesessionId,
            name=session_name
        )
        
        db.add(new_conversation)
        await db.flush()
        
        await db.commit()
        
        return {
            "conversation_id": new_conversation.id,
            "session_id": new_conversation.session_id,
            "name": new_conversation.name
        }        
        
    except Exception as E:
        db.rollback()
        raise E