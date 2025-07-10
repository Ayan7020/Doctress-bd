from langchain_groq import ChatGroq
from core.config import settings

GroqLLm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=settings.GROQ_API_KEY_LLM
)