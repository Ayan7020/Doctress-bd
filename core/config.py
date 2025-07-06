from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NEON_CONNECTION_STR: str
    PINECONE_API_KEY: str
    GROQ_API_KEY_LLM: str
    REDIS_CONNECTION_URL: str
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()