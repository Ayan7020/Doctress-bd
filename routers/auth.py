from fastapi import APIRouter , Depends
from core.database import get_db
from services.auth.signupController import SignupsendOtpController
from services.auth.LoginController import LoginCredentialController
from schemas.auth.signup import SignupModel
from schemas.auth.login import LoginModel
from fastapi import Request , Response
from fastapi.exceptions import RequestValidationError
from contextlib import closing
from sqlalchemy import text 
from utils.authUtils import AuthUtilsManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

router = APIRouter()

@router.post("/signup")
async def Signup(data: SignupModel,db = Depends(get_db)):
    """Send Otp to User for Verification of Email"""
    return await SignupsendOtpController(data,db) 

@router.post("/login")
async def Signup(data: LoginModel,db = Depends(get_db)):
    """Login the user and set's cookies for access and refresh token"""
    return await LoginCredentialController(data,db) 

@router.get("/refresh-token")
async def CreateAccessToken(req: Request,res: Response,db: AsyncSession = Depends(get_db)):
    try:  
        refresh_token = req.cookies.get("refresh_token")
        
        if not refresh_token:
            raise RequestValidationError("Refresh Token not found")  
        
        VerifiedrefreshToken: dict = await AuthUtilsManager.VerifyRefreshToken(refresh_token)
         
        if not VerifiedrefreshToken:
            raise RequestValidationError("Invalid Refresh Token")
        query = select(User).where(User.email == VerifiedrefreshToken.get("email"))
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()
        
          
        if not existing_user:
            return RequestValidationError("User not found")
        
        payload = {
            "userId": str(existing_user.id),
            "email": existing_user.email
        }
        access_token = AuthUtilsManager.GenerateAccessToken(payload) 
        res.set_cookie("access_token", access_token, httponly=True, samesite="none",secure=True, max_age=900)

        return {
            "message": "Access token Updation completed"
        }
        
    except Exception as e: 
        raise e