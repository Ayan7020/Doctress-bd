from sqlalchemy import Column, Integer, String, DateTime, func , ForeignKey
from sqlalchemy.orm import declarative_base , relationship 
from models.base import Base 

class UploadedFile(Base):
    __tablename__ = 'uploadedfile'

    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    email = Column(String, index=True) 
    companyName = Column(String, nullable=False)
    department = Column(String, nullable=False)
    blob_url = Column(String)
    filename = Column(String, nullable=False)  
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="uploaded_files")