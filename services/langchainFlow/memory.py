from langchain.memory import ConversationTokenBufferMemory
from services.langchainFlow.llm import GroqLLm
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables import RunnableLambda
from core.redis_client import redis_client
from core.config import settings

def get_memory(session_id: str): 
    history = RedisChatMessageHistory(session_id=session_id,url=settings.REDIS_CONNECTION_URL)
 
    memory = ConversationTokenBufferMemory(
        llm=GroqLLm,
        memory_key="chat_history",
        chat_memory=history,
        return_messages=True,
        max_token_limit=700
    )
    
    
    return memory
 
 
MemoryRetrievalLambda = RunnableLambda(lambda input: get_memory(input["session_id"]).load_memory_variables(input)["chat_history"])