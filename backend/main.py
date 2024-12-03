import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.database_manager import DatabaseManager
from backend.api.v1.routes import router as api_router
from backend.utils.logging_utils import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database instance
database = DatabaseManager.get_instance()

@app.on_event("startup")
async def startup():
    """Initialize database connection and schema on startup."""
    try:
        await database.initialize()
        log_info("Database connection established successfully")
    except Exception as e:
        log_error(f"Failed to initialize database: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown."""
    try:
        await database.close()
        log_info("Database connection closed successfully")
    except Exception as e:
        log_error(f"Error closing database connection: {str(e)}")
        raise

# Include the API router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
