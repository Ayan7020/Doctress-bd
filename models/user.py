from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base , relationship
from models.base import Base 
 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    companyName = Column(String, nullable=False)
    department = Column(String, nullable=False)
    
    uploaded_files = relationship("UploadedFile", back_populates="user", cascade="all, delete-orphan")
    conversation = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")