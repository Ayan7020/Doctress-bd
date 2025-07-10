from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from models.base import Base  # Make sure Base = declarative_base()

class ChatMemory(Base):
    __tablename__ = 'chatmemory'

    id = Column(Integer, primary_key=True, index=True)
    
    conversation_id = Column(Integer, ForeignKey("conversation.id", ondelete="CASCADE"), nullable=False)
    
    query = Column(String, nullable=False, index=True)
    output = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
     
    conversation = relationship("Conversation", back_populates="chatmemory")
