# database/database.py

import os
import asyncpg
import threading

from backend.database.migration_manager import MigrationManager
from backend.constants.const import *
from backend.utils.logging_utils import *

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

class DatabaseManager:
    _lock = threading.Lock()
    _instance = None

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection = None
        self.migration_manager = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(dsn=DATABASE_URL)
        return cls._instance

    async def initialize(self):
        """Initialize database connection and check for schema changes"""
        try:
            # Connect to database
            self.connection = await asyncpg.connect(self.dsn)
            
            # Initialize migration manager
            self.migration_manager = MigrationManager(self.connection)
            
            # Check and apply any schema changes
            await self.migration_manager.check_for_changes()
            
            log_info("Database initialization completed successfully")
        except Exception as e:
            log_error(f"Error initializing database: {str(e)}")
            raise

    async def close(self):
        """Close the database connection"""
        if self.connection:
            await self.connection.close()
