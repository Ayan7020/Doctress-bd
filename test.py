# import bcrypt

# def hash_password(plain_password: str) -> str:
#     """Hash a plain text password using bcrypt."""
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
#     return hashed.decode('utf-8')   

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



# print(hash_password("Cukoo@702002"))
# print(verify_password("Cukoo@702002sdsd","$2b$12$phzc62T9qTebuqcCiq9ZouDGRuZgu5/Tb17ejC0p7TEbsIErbmCJu")) 


import redis.asyncio as redis
from core.config import settings

redis_client = redis.from_url(
    settings.REDIS_CONNECTION_URL,
    decode_responses=True  
)