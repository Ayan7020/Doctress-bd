from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import traceback

class ExceptionHandler:
    
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        print(f"HTTPException: {exc.detail} | Path: {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
            "success": False,
            "error": {
                    "type": "HTTPException",
                    "message": exc.detail
            }
        })
    
    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        print(f"Validation error: {exc.errors()} | Body: {exc.body}")
        return JSONResponse(
            status_code=422,
            content={
            "success": False,
            "error": {
                    "type": "ValidationError",
                    "message": "Invalid request parameters",
                    "details": exc.errors()
                }
        })
    
    @staticmethod
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        print(f"Database error: {str(exc)} | Path: {request.url}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": "DatabaseError",
                    "message": "A database error occurred"
                }
            },
        )
    
    @staticmethod
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        print(f"Unhandled exception: {str(exc)} | Trace: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred"
                }
            },
        )
    
    
    
    