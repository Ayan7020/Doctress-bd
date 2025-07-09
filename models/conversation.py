from sqlalchemy import Column, Integer, String, DateTime, func , ForeignKey
from sqlalchemy.orm import  relationship 
from models.base import Base 

class Conversation(Base):
    __tablename__ = 'conversation'
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
    session_id = Column(String,unique=True,nullable=False)
    name = Column(String,unique=True,nullable=False)
    
    user = relationship("User", back_populates="conversation")