from fastapi import APIRouter , UploadFile as UploadFileType , File , Form , HTTPException , Depends
from middleware.isAuthenticated import is_authenticated
from services.ExecutiveUser.UploadPdfControllers import UploadPdfController
router = APIRouter(
    dependencies=[Depends(is_authenticated)]
)

@router.post("/uploadpdf")
async def uploadPdf(uploadpdf: UploadFileType = File(...),fileName: str = Form(...),department: str = Form(...)):
    """Upload the file to Azure Blob Storage and send pdf to Queue for processing"""
    return await UploadPdfController(uploadpdf,fileName,department)
    
    
    
    