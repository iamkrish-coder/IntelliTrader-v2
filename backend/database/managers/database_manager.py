# database/database.py

import os
import asyncpg
import threading
from typing import Optional, Any, Dict, List
from datetime import datetime
from dotenv import load_dotenv

from backend.database.managers.migration_manager import MigrationManager
from backend.constants.const import *
from backend.utils.logging_utils import *

load_dotenv()
DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

class DatabaseConnectionError(Exception):
    """Custom exception for database connection errors"""
    pass

class DatabaseManager:
    _lock = threading.Lock()
    _instance = None

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
        self.migration_manager = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(dsn=DATABASE_URL)
        return cls._instance

    async def initialize(self):
        """Initialize database pool and check for schema changes"""
        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=5,
                max_size=20,
                command_timeout=60,
                max_inactive_connection_lifetime=300.0,
                timeout=30.0
            )
            
            if not self.pool:
                raise DatabaseConnectionError("Failed to create database pool")

            async with self.pool.acquire() as connection:
                self.migration_manager = MigrationManager(connection)
                await self.migration_manager.check_for_changes()
            
            log_info("Database pool initialized successfully")
            
        except (OSError, asyncpg.PostgresConnectionError) as e:
            if "Connect call failed" in str(e):
                raise DatabaseConnectionError(
                    "Could not connect to PostgreSQL database. Please ensure that:\n"
                    "1. The PostgreSQL Docker container is running\n"
                    "2. The database credentials in .env are correct\n"
                    "3. The database port (default: 5432) is not in use"
                ) from e
            raise DatabaseConnectionError(f"Database connection failed: {str(e)}") from e
        except Exception as e:
            log_error(f"Error initializing database pool: {e}")
            raise

    def get_connection_pool(self):
        """
        Return the current database connection pool.
        """
        if not self.pool:
            raise Exception("Database pool not initialized. Call initialize() first.")
        return self.pool

    async def call_procedure(
        self,
        procedure_name: str,
        *args: Any,
        transaction: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a stored procedure
        """
        try:
            async with self.pool.acquire() as conn:
                # Simple parameter placeholders
                param_placeholders = [f"${i+1}" for i in range(len(args))]
                params = ", ".join(param_placeholders)
                
                # Construct the query
                query = f"CALL {procedure_name}({params})"
                
                # Execute the query
                if transaction:
                    async with conn.transaction():
                        result = await conn.fetch(query, *args)
                else:
                    result = await conn.fetch(query, *args)
                
                return {
                    "success": result[0][0] if result and len(result) > 0 else False,
                    "message": result[0][1] if result and len(result) > 0 else "",
                    "data": result[0][2] if result and len(result) > 0 else None
                }
                
        except Exception as e:
            log_error(f"Error executing procedure {procedure_name}: {str(e)}")
            return {
                "success": False,
                "message": f"Error executing procedure: {str(e)}",
                "data": None
            }

    async def call_function(
        self,
        function_name: str,
        *args: Any,
        fetch_mode: str = 'all',
        transaction: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a database function
        fetch_mode: 'all' | 'one' | 'value'
        """
        try:
            async with self.pool.acquire() as conn:
                if transaction:
                    async with conn.transaction():
                        result = await self._execute_function(conn, function_name, args, fetch_mode)
                else:
                    result = await self._execute_function(conn, function_name, args, fetch_mode)

                return {
                    "success": True,
                    "data": result
                }
        except Exception as e:
            log_error(f"Error executing function {function_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _execute_function(
            self,
            conn: asyncpg.Connection,
            function_name: str,
            args: tuple,
            fetch_mode: str
        ) -> Any:
            """
            Execute function with specified fetch mode
            """
            # Create parameter placeholders based on number of arguments
            placeholders = ', '.join(f'${i+1}' for i in range(len(args)))
            query = f'SELECT * FROM {function_name}({placeholders})'
            
            if fetch_mode == 'all':
                result = await conn.fetch(query, *args) 
                return [dict(r) for r in result]
            elif fetch_mode == 'one':
                result = await conn.fetchrow(query, *args)
                return dict(result) if result else None              
            elif fetch_mode == 'value':
                return await conn.fetchval(query, *args)
            else:
                raise ValueError(f"Invalid fetch_mode: {fetch_mode}")

    async def close(self):
        """Close the database pool"""
        if self.pool:
            await self.pool.close()
            log_info("Database pool closed")
