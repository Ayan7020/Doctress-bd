from fastapi import APIRouter , Depends
from fastapi import Request

from middleware.isAuthenticated import is_authenticated
 
router = APIRouter(
        
)

@router.get("/get-logged-in-user")
async def GetLoggedInUser(req: Request):
    """Get the loggedin user based on the AccessToken"""
    Data = req.state.user 
    return {
        "status": True,
        "Message": Data.email
    }

