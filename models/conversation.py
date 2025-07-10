from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Conversation(Base):
    __tablename__ = 'conversation'

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    session_id = Column(String, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="conversation")
    chatmemory = relationship("ChatMemory", back_populates="conversation", cascade="all, delete-orphan")
