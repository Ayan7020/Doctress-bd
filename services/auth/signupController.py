from schemas.auth.signup import SignupModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from fastapi import HTTPException
from utils.authUtils import AuthUtilsManager

async def SignupsendOtpController(data: SignupModel,db: AsyncSession):
    """Send the Otp to the user for verification of Signup"""
    try: 
        stmt = select(User).where(User.email == data.email)
        result = await db.execute(stmt)
        user_exists = result.scalar_one_or_none()
        
        if user_exists:
            raise HTTPException(status_code=409, detail="User already exists with this email")
        
        AuthUtilsManager.CheckOtpRestriction(data.email)
        
    except Exception as E:
        await db.rollback()
        raise E
    
async def VerifySignupOtpController(data,db: AsyncSession):
    """Verify the otp and create the user"""
    pass