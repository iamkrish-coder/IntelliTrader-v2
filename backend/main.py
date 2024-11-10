import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.database_manager import DatabaseManager, sqlalchemy_engine, Base
from backend.api.v1.routes import router as api_router

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
async def on_startup():
    await database.connect()

    # Create tables if they do not exist
    async with database.sqlalchemy_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize all stored procedures
    await database.check_for_upgrade()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
