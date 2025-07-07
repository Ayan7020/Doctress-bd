from fastapi import APIRouter , Depends
from core.database import get_db
from services.auth.signupController import SignupsendOtpController
from schemas.auth.signup import SignupModel
router = APIRouter()

@router.post("/signup")
async def Signup(data: SignupModel,db = Depends(get_db)):
    """Send Otp to User for Verification of Email"""
    return await SignupsendOtpController(data,db) 