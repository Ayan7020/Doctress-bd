from schemas.conversation.message import MessageModel
from services.langchainFlow.chain import MainChain
from services.langchainFlow.memory import get_memory
from fastapi import Request
from fastapi.responses import StreamingResponse
from models.chatMemory import ChatMemory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

async def create_message_controller(req: Request, data: MessageModel, db: AsyncSession):
    """
    Streams LLM response, updates LangChain memory, and saves chat to DB.
    """
    try:
        user = req.state.user

        input_payload = {
            "query": data.query,
            "companyName": user.companyName,
            "department": user.department,
            "session_id": data.session_id
        }

        memory = get_memory(data.session_id)
         

        async def token_stream():
            collected = ""
            try:
                async for chunk in MainChain.astream(input_payload):
                    print("Chunk",chunk)
                    collected += chunk
                    yield chunk
 
                memory.save_context(
                    {"input": data.query},
                    {"output": collected}
                )
 
                db_memory = ChatMemory(
                    conversation_id=data.conversation_id,
                    query=data.query,
                    output=collected
                )
                
                db.add(db_memory)
                
                await db.commit()
                
            except SQLAlchemyError as db_err:
                await db.rollback()
                raise db_err
            
            except Exception as stream_err:
                raise stream_err

        return StreamingResponse(token_stream(), media_type="text/plain")

    except Exception as e:
        raise e
