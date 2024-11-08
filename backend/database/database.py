# database/database.py

import os
import asyncpg
import threading
import logging
import importlib

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Any, List
from backend.utils.logging_utils import *
from backend.constants.const import PROCEDURES_DIR

# DSN for asyncpg (stored procedures and direct SQL execution)
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# DSN for SQLAlchemy async engine (if used for initial table creation)
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# SQLAlchemy engine (for table setup only)
sqlalchemy_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=sqlalchemy_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class Database:
    _lock = threading.Lock()
    _instance = None

    def __init__(self, dsn: str, sqlalchemy_dsn: str):
        self.dsn = dsn
        self.sqlalchemy_dsn = sqlalchemy_dsn
        self.asyncpg_connection = None
        self.sqlalchemy_engine = None
        self.sqlalchemy_session_local = None


    async def connect(self):
        """Set up the asyncpg connection and SQLAlchemy session engine."""
        # Connect using asyncpg (for stored procedures and raw SQL)
        self.asyncpg_connection = await asyncpg.connect(dsn=self.dsn)
        
        # Set up SQLAlchemy engine and session
        self.sqlalchemy_engine = create_async_engine(self.sqlalchemy_dsn, echo=True)
        
        self.sqlalchemy_session_local = sessionmaker(
            bind=self.sqlalchemy_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )


    async def disconnect(self):
        await self.asyncpg_connection.close()
        await self.sqlalchemy_engine.dispose()

    
    async def get_session(self) -> AsyncSession:
        """Create and return an SQLAlchemy session."""
        session = self.sqlalchemy_session_local()
        return session


    async def execute_stored_procedure(self, sp_name: str, *params) -> List[Any]:
        """Executes a stored procedure with the provided name and parameters."""
        async with self.asyncpg_connection.transaction():

            # Create a string of placeholders for the parameters
            placeholders = ', '.join(f'${i + 1}' for i in range(len(params)))
            result = await self.asyncpg_connection.fetch(
                f'CALL {sp_name}({placeholders})',
                *params
            )
        return result


    async def initialize_all_procedures(self) -> List[Any]:
        """Executes all stored procedures found in the backend.database.procedures directory."""
        results = []

        for module_name in os.listdir(PROCEDURES_DIR):
            module_path = os.path.join(PROCEDURES_DIR, module_name)
            if os.path.isdir(module_path):
                for filename in os.listdir(module_path):
                    if filename.endswith('.sql'):
                        file_path = os.path.join(module_path, filename)
                        with open(file_path, 'r') as file:
                            sql_command = file.read()

                        # Modify the SQL command with module prefix (lowercase for PostgreSQL)
                        sql_command = sql_command.replace('CALL', f'CALL {module_name.lower()}.')

                        try:
                            # Execute the SQL command
                            result = await self.asyncpg_connection.execute(sql_command)
                            results.append((file_path, result))
                        except Exception as error:
                            # Log error without halting the startup
                            log_error(f"Error executing {file_path}: {error}")

        return results


    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(dsn=DATABASE_URL, sqlalchemy_dsn=SQLALCHEMY_DATABASE_URL)
        return cls._instance