import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Tuple
from backend.utils.logging_utils import *

class MigrationManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.definitions_dir = os.path.join(self.base_dir, "database", "definitions")
        self.routines_dir = os.path.join(self.base_dir, "database", "routines")
        self.version_file = os.path.join(self.base_dir, "database", "version_control", "schema_version.json")

    def _get_utc_now(self) -> str:
        """Get current UTC time in ISO format"""
        return datetime.datetime.now(timezone.utc).isoformat()

    async def check_for_changes(self):
        """Check for changes in table definitions and database routines"""
        try:
            # Initialize or load schema state
            schema_state = await self.get_schema_state()
            
            # Check tables
            await self._check_table_changes(schema_state)
            
            # Check stored procedures
            await self._check_routine_changes(schema_state, "procedures")
            
            # Check functions
            await self._check_routine_changes(schema_state, "functions")
            
            log_info("Database upgrade checks completed successfully")
        except Exception as e:
            log_error(f"Error checking for database schema changes: {str(e)}")
            raise

    async def get_schema_state(self) -> Dict:
        """Get current schema state from version file"""
        if not os.path.exists(self.version_file):
            return {
                "metadata": {
                    "current_version": 0,
                    "last_updated": self._get_utc_now()
                },
                "tables": {},
                "procedures": {},
                "functions": {}
            }
        
        with open(self.version_file, 'r') as f:
            return json.load(f)

    def _get_next_version(self, schema_state: Dict) -> int:
        """Get next version number for migrations"""
        current_version = schema_state.get("metadata", {}).get("current_version", 0)
        return current_version + 1

    async def _update_schema_state(self, schema_state: Dict, object_type: str, object_key: str, new_checksum: str):
        """Update schema state with new version information"""
        # Increment version
        new_version = self._get_next_version(schema_state)
        current_time = self._get_utc_now()
        current_date = datetime.datetime.now(timezone.utc).strftime('%Y%m%d')
        
        # Update metadata
        schema_state["metadata"] = {
            "current_version": new_version,
            "last_updated": current_time
        }
        
        # Update object state
        schema_state[object_type][object_key] = {
            "version": f"V{new_version}",
            "checksum": new_checksum,
            "last_modified": current_time,
            "migration_id": f"V{new_version}_{current_date}_{object_key}"
        }
        
        # Save updated schema state
        with open(self.version_file, 'w') as f:
            json.dump(schema_state, f, indent=4)
        
        return schema_state

    async def _check_table_changes(self, schema_state: Dict):
        """Check for changes in table definitions"""
        for root, _, files in os.walk(self.definitions_dir):
            for file in files:
                if file.endswith('.sql'):
                    table_file = os.path.join(root, file)
                    new_checksum = self._calculate_checksum(table_file)
                    
                    module, table = self._parse_table_info(table_file)
                    table_key = f"{module}.{table}"
                    
                    if (table_key not in schema_state["tables"] or 
                        schema_state["tables"][table_key]["checksum"] != new_checksum):
                        await self._handle_table_change(table_file, new_checksum, schema_state)

    async def _check_routine_changes(self, schema_state: Dict, routine_type: str):
        """Check for changes in stored procedures or functions"""
        routines_path = os.path.join(self.routines_dir, routine_type)
        if not os.path.exists(routines_path):
            return

        for root, _, files in os.walk(routines_path):
            for file in files:
                if file.endswith('.sql'):
                    routine_file = os.path.join(root, file)
                    new_checksum = self._calculate_checksum(routine_file)
                    
                    module, routine = self._parse_routine_info(routine_file)
                    routine_key = f"{module}.{routine}"
                    
                    if (routine_key not in schema_state[routine_type] or 
                        schema_state[routine_type][routine_key]["checksum"] != new_checksum):
                        await self._handle_routine_change(routine_file, new_checksum, routine_type, schema_state)

    async def _handle_routine_change(self, routine_file: str, new_checksum: str, routine_type: str, schema_state: Dict):
        """Handle changes in stored procedures or functions"""
        try:
            # Read the routine definition
            with open(routine_file, 'r') as f:
                routine_sql = f.read()

            # Drop existing routine if it exists
            module, routine = self._parse_routine_info(routine_file)
            drop_sql = f"DROP {routine_type.upper()} IF EXISTS {module}.{routine} CASCADE;"
            
            async with self.db.transaction():
                # Drop existing routine
                await self.db.execute(drop_sql)
                # Create new routine
                await self.db.execute(routine_sql)

            # Update schema state
            routine_key = f"{module}.{routine}"
            schema_state = await self._update_schema_state(schema_state, routine_type, routine_key, new_checksum)
            
            log_info(f"Successfully updated {routine_type}: {routine_key}")
        except Exception as e:
            log_error(f"Error handling {routine_type} change: {str(e)}")
            raise

    async def _handle_table_change(self, table_file: str, new_checksum: str, schema_state: Dict):
        """Handle changes in table definitions"""
        try:
            # Read the table definition
            with open(table_file, 'r') as f:
                table_sql = f.read()

            # Execute the table definition
            async with self.db.transaction():
                await self.db.execute(table_sql)

            # Update schema state
            module, table = self._parse_table_info(table_file)
            table_key = f"{module}.{table}"
            schema_state = await self._update_schema_state(schema_state, "tables", table_key, new_checksum)
            
            log_info(f"Successfully updated table: {table_key}")
        except Exception as e:
            log_error(f"Error handling table change: {str(e)}")
            raise

    def _parse_routine_info(self, routine_file: str) -> Tuple[str, str]:
        """Extract module and routine name from file path"""
        relative_path = os.path.relpath(routine_file, self.routines_dir)
        parts = relative_path.split(os.sep)
        module = parts[0].upper()  # First directory is module name
        routine = os.path.splitext(parts[-1])[0]  # File name without extension
        return module, routine

    def _parse_table_info(self, table_file: str) -> Tuple[str, str]:
        """Extract module and table name from file path"""
        relative_path = os.path.relpath(table_file, self.definitions_dir)
        parts = relative_path.split(os.sep)
        module = parts[0].upper()  # First directory is module name
        table = os.path.splitext(parts[-1])[0]  # File name without extension
        return module, table

    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
