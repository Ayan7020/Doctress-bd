from fastapi import FastAPI
from core.config import settings
import uvicorn

app = FastAPI(
    title="Docfortress APIs",
    description="Backend APIs for the Docfortress application.",
    version="1.0.0"
)

@app.get("/health", tags=["Health Check"])
def get_health():
    """Check the health of the application."""
    return {
        "success": True,
        "message": "Good"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
