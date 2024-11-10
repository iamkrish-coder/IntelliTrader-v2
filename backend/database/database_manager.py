# database/database.py

import os
import asyncpg
import threading
import logging
import importlib
import hashlib
import json

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Any, List

from backend.database.database_upgrade import DatabaseUpgrade

from backend.utils.logging_utils import *
from backend.enumerations.enums import *
from backend.constants.const import *



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

class DatabaseManager:
    _lock = threading.Lock()
    _instance = None

    def __init__(self, dsn: str, sqlalchemy_dsn: str):
        self.dsn = dsn
        self.sqlalchemy_dsn = sqlalchemy_dsn
        self.asyncpg_connection = None
        self.sqlalchemy_engine = None
        self.sqlalchemy_session_local = None
        self.db_updates_dir = DB_UPDATES_DIR
        self.db_routines_dir = DB_ROUTINES_DIR

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(dsn=DATABASE_URL, sqlalchemy_dsn=SQLALCHEMY_DATABASE_URL)
        return cls._instance

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

            placeholders = ', '.join(f'${i + 1}' for i in range(len(params)))
            query = f'CALL {sp_name}({placeholders})'
            result = await self.asyncpg_connection.fetch(query, *params)
        return result

    async def execute_function(self, fn_name: str, *params, multiple: bool = True) -> List[Any] | Any:
        """Executes a function with the provided name and parameters."""
        async with self.asyncpg_connection.transaction():

            placeholders = ', '.join(f'${i + 1}' for i in range(len(params)))
            query = f'SELECT * FROM {fn_name}({placeholders})'

            if multiple:
                result = await self.asyncpg_connection.fetch(query, *params)
            else:
                result = await self.asyncpg_connection.fetchrow(query, *params)

            # Flatten if the result is nested
            if result and isinstance(result[0], asyncpg.Record):
                flattened_result = [
                    record[fn_name] if fn_name in record else record for record in result
                ]
                return flattened_result if multiple else flattened_result[0]
            
        return result

    async def check_for_upgrade(self):
        # Call the check_for_updates method when needed
        database_upgrade = DatabaseUpgrade(self.asyncpg_connection, self.db_updates_dir, self.db_routines_dir)
        await database_upgrade.check_for_updates()
