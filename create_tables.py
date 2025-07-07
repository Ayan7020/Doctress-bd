
import asyncio
from core.database import engine
from models.user import Base

async def create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create())
