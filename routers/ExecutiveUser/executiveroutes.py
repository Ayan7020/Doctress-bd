from fastapi import APIRouter , UploadFile as UploadFileType , File , Form , HTTPException , Depends ,Request
from middleware.isAuthenticated import is_authenticated
from services.ExecutiveUser.UploadPdfControllers import UploadPdfController
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    dependencies=[Depends(is_authenticated)]
)

@router.post("/uploadpdf")
async def uploadPdf(req: Request,uploadpdf: UploadFileType = File(...),fileName: str = Form(...),department: str = Form(...),db: AsyncSession = Depends(get_db)):
    """Upload the file to Azure Blob Storage and send pdf to Queue for processing"""
    return await UploadPdfController(req,uploadpdf,fileName,department,db)
    
    
    
    