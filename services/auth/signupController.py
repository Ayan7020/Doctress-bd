from schemas.auth.signup import SignupModel
from sqlalchemy.orm import Session

async def SignupsendOtpController(data: SignupModel,db: Session):
    """Send the Otp to the user for verification of Signup"""
    try:
        pass
    except Exception as E:
        raise E
    
async def VerifySignupOtpController(data,db: Session):
    """Verify the otp and create the user"""
    pass