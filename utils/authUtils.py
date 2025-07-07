from core.redis_client import redis_client
from fastapi.exceptions import HTTPException
import bcrypt
from datetime import datetime , timedelta
import os 
from jose import jwt , JWTError
from core.config import settings

class AuthUtilsManager:
    CoolDownKey = "otp_cooldown"
    SpamKey = "otp_spam"
    otpLock = "otp_lock"
     
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    @staticmethod
    async def CheckOtpRestriction(email: str):
        try:
            if await redis_client.get(f"{AuthUtilsManager.SpamKey}:{email}"):
                raise HTTPException(
                    status_code=429,
                    detail="Too many OTP requests! Please wait 1 hour before sending a new request."
                )
            
            if await redis_client.get(f"{AuthUtilsManager.CoolDownKey}:{email}"):
                raise HTTPException(
                    status_code=429,
                    detail="Please wait 1 minute before requesting a new OTP."
                )
            
            if await redis_client.get(f"{AuthUtilsManager.otpLock}:{email}"):
                raise HTTPException(
                    status_code=423,
                    detail="Account locked due to multiple failed attempts! Try again after 30 minutes."
                )
            
        except Exception as E:
            raise E
    
    @staticmethod
    async def VerifyPassword(plain_password: str,hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    async def GenerateToken(payload: dict,exp,token: str):
        """return Jwt Token """
        payload.update({"exp": exp})
        return jwt.encode(payload,token, algorithm="HS256")
    
    @staticmethod
    async def GenerateAccessToken(payload: dict):
        data = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=AuthUtilsManager.ACCESS_TOKEN_EXPIRE_MINUTES)
        return await AuthUtilsManager.GenerateToken(data,expire,settings.JWT_ACCESS_SECRET)
    
    @staticmethod
    async def GenerateRefreshToken(payload: dict):
        data = payload.copy()
        expire = datetime.utcnow() + timedelta(days=AuthUtilsManager.REFRESH_TOKEN_EXPIRE_DAYS)
        return await AuthUtilsManager.GenerateToken(data,expire,settings.JWT_REFRESH_SECRET)
    
    @staticmethod
    async def VerifyRefreshToken(token: str): 
        payload = jwt.decode(token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"])
        return payload  
    
    @staticmethod
    async def VerifyAccessToken(token: str):
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=["HS256"])
        return payload  
        
        
    
        
        