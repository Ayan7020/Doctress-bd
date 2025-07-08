from fastapi import APIRouter , UploadFile as UploadFileType , File , Form , HTTPException , Depends

async def UploadPdfController(uploadpdf: UploadFileType,fileName: str,department: str):
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
    
    return {
        "success": True,
        "message": "File uploaded for processing", 
        "filename": fileName,
        "department": department
    }