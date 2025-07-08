from fastapi import APIRouter , UploadFile as UploadFileType , File , Form , HTTPException , Depends , Request
from core.rabbitmq import rabbitmq
from sqlalchemy.future import select
from models.filesUser import UploadedFile
from core.AzureBlob import AzureBlobObj
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

async def UploadPdfController(req: Request,uploadpdf: UploadFileType,fileName: str,department: str,db: AsyncSession):
    """Validates file and performs upload + queue operation"""
    
    allowed_extensions = (".pdf", ".docx", ".csv")
    if not  uploadpdf.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Only PDF , CSV or DOCX allowed")
    
    
    allowed_departments = {"finance", "marketing", "hr","engineering","employee"}
    if department.lower() not in allowed_departments:
        raise HTTPException(status_code=400, detail="Invalid department")
    
    allowed_mime_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/csv",
        "application/vnd.ms-excel"   
    }
    if uploadpdf.content_type not in allowed_mime_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_data = await uploadpdf.read()
    
    blob_result = AzureBlobObj.upload_file(
        file_data=file_data,
        content_type=uploadpdf.content_type,
        original_filename=fileName
    ) 
    
    user = req.state.user
    
    new_file = UploadedFile(
        user_id=user.id,
        email=user.email,
        companyName=user.companyName,
        department=department,
        blob_url=blob_result["blob_url"],
        filename=fileName,
    )
    
    db.add(new_file)
    
    await db.commit()
    await db.refresh(new_file)
    
    await rabbitmq.publish(
        queue_name='uploaddocs',
        message={
            "email": user.email,
            "blob_url": blob_result["blob_url"],
            "userId": str(user.id),
            "department": department,
            "companyName": user.companyName
        }
    )
    
    return {
        "success": True,
        "message": "File uploaded for processing", 
        "blob_url": blob_result["blob_url"],
        "stored_filename": blob_result["blob_name"],
        "filename": fileName,
        "department": department
    }