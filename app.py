from fastapi import FastAPI
from core.config import settings
import uvicorn
from utils.Exception.ExceptionHandler import ExceptionHandler
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError 
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import router as AuthRouter
from routers.user import router as UserRouter
 

app = FastAPI(
    title="Docfortress APIs",
    description="Backend APIs for the Docfortress application.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"]
)

app.add_exception_handler(StarletteHTTPException,ExceptionHandler.http_exception_handler)
app.add_exception_handler(RequestValidationError, ExceptionHandler.validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, ExceptionHandler.sqlalchemy_exception_handler)
app.add_exception_handler(Exception, ExceptionHandler.generic_exception_handler)

@app.get("/health", tags=["Health Check"])
def get_health():
    """Check the health of the application."""
    return {
        "success": True,
        "message": "Good"
    }
    
app.include_router(AuthRouter,tags=["Auth"])
app.include_router(UserRouter,tags=["User"])

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)
