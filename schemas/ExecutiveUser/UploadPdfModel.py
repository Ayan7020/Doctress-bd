from pydantic import BaseModel 
from fastapi import UploadFile

class SignupModel(BaseModel):
    email: str
    UploadFile: str 