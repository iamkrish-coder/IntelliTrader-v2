import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.database.managers.database_manager import DatabaseManager, DatabaseConnectionError
from backend.api.v1.routes import router as api_router
from backend.utils.logging_utils import *
from backend.core.middleware import error_handling_middleware

app = FastAPI()

# Add error handling middleware first
app.middleware("http")(error_handling_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
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
        log_info("Database connected")
    except DatabaseConnectionError as e:
        log_error(str(e))
        # We don't raise here to allow the application to start without the database
        # This way we can show a proper error message to API clients
    except Exception as e:
        log_error(f"Unexpected error during startup: {str(e)}")
        raise

@app.middleware("http")
async def check_database_connection(request, call_next):
    if database.pool is None:
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Database connection is not available. Please check server logs for details."
            }
        )
    return await call_next(request)

@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown."""
    try:
        await database.close()
        log_info("Database connection closed")
    except Exception as e:
        log_error(f"Error closing database connection: {str(e)}")
        raise

# Include the API router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
