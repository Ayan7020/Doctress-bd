from pydantic import BaseModel 
from fastapi import UploadFile 

class UploadFileModel(BaseModel): 
    uploadfile: UploadFileType
    filename: str 
    department: str