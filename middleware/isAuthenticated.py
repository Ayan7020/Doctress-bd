# dependencies/is_authenticated.py
from fastapi import Request, HTTPException, Depends
from utils.authUtils import AuthUtilsManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from core.database import get_db

async def is_authenticated(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access Token missing")

    verifyToken = await AuthUtilsManager.VerifyAccessToken(token)
    if not verifyToken:
        raise HTTPException(status_code=401, detail="Invalid Access Token")

    query = select(User).where(User.id == int(verifyToken.get("userId")))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    request.state.user = user  # Store for access in route
