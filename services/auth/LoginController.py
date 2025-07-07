from schemas.auth.signup import SignupModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from fastapi import HTTPException
from utils.authUtils import AuthUtilsManager
from fastapi.responses import JSONResponse

async def LoginCredentialController(data: SignupModel,db: AsyncSession):
    """Login The User and if everything works greate assign it access and refresh token in cookies"""
    try: 
        stmt = select(User).where(User.email == data.email)
        result = await db.execute(stmt)
        user_exists = result.scalar_one_or_none()
        
        if not user_exists:
            raise HTTPException(status_code=409, detail="User doesn't exists with this email")
        
        verifyPass = await AuthUtilsManager.VerifyPassword(data.password,user_exists.password)
        
        if not verifyPass:
            raise HTTPException(status_code=409, detail="Email or Password is uncorrect")
        
        payload = {
            "userId": str(user_exists.id),
            "email": user_exists.email
        }
        
        access_token = await AuthUtilsManager.GenerateAccessToken(payload)
        refresh_token = await AuthUtilsManager.GenerateRefreshToken(payload)
        
        response = JSONResponse(content={"message": "Login successful"}, status_code=200)
        response.set_cookie("access_token", access_token, httponly=True, samesite="lax",secure=False, max_age=900)
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax",secure=False, max_age=604800)
        return response
        
    except Exception as E:
        await db.rollback()
        raise E
    
async def VerifySignupOtpController(data,db: AsyncSession):
    """Verify the otp and create the user"""
    pass