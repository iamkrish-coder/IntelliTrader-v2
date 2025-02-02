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
        self.definitions_dir = os.path.join(self.base_dir, "definitions")
        self.procedures_dir = os.path.join(self.base_dir, "procedures")
        self.functions_dir = os.path.join(self.base_dir, "functions")
        self.version_file = os.path.join(self.base_dir, "version_control", "schema_version.json")
        self._changes_made = False

    def _get_utc_now(self) -> str:
        """Get current UTC time in ISO format"""
        return datetime.datetime.now(timezone.utc).isoformat()

    async def check_for_changes(self):
        """Check for changes in table definitions and database routines"""
        try:
            # Initialize or load schema state
            schema_state = await self.get_schema_state()
            initial_version = schema_state["metadata"]["current_version"]
            
            # Reset changes tracker
            self._changes_made = False
            
            # Check and install tables
            await self._check_and_install_tables(schema_state)
            
            # Check and install stored procedures
            await self._check_and_install_routines(schema_state, self.procedures_dir, "procedures")
            
            # Check and install functions
            await self._check_and_install_routines(schema_state, self.functions_dir, "functions")
            
            # Only log if changes were made
            if self._changes_made:
                log_info("Database schema version updated successfully")
            else:
                log_info("No changes detected in database schema")
        except Exception as e:
            log_error(f"Error during database upgrade checks: {e}")

    async def get_schema_state(self) -> Dict:
        """Load the current schema state from the version file"""
        if not os.path.exists(self.version_file):
            return {
                "metadata": {
                    "current_version": 1,
                    "last_updated": self._get_utc_now()
                },
                "definitions": {},
                "procedures": {},
                "functions": {}
            }
        with open(self.version_file, 'r') as f:
            return json.load(f)

    async def _check_and_install_tables(self, schema_state: Dict):
        """Check and install tables if there are changes"""
        table_files = os.listdir(self.definitions_dir)
        changes_detected = False
        
        for table_file in table_files:
            table_path = os.path.join(self.definitions_dir, table_file)
            with open(table_path, 'r') as f:
                table_sql = f.read()
            table_hash = hashlib.sha256(table_sql.encode()).hexdigest()
            table_name = os.path.splitext(table_file)[0].lower()
            
            # Check if table exists
            table_exists_query = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"
            table_exists = await self.db.fetchval(table_exists_query)
            
            # Install table if it doesn't exist or definition has changed
            if not table_exists or schema_state["definitions"].get(table_name, {}).get("checksum") != table_hash:
                await self._install_table(table_name, table_sql)
                schema_state["definitions"][table_name] = {
                    "checksum": table_hash,
                    "last_modified": self._get_utc_now()
                }
                schema_state["metadata"]["current_version"] += 1
                changes_detected = True
                self._changes_made = True
                log_info(f"Table {table_name} {'created' if not table_exists else 'updated'}")
        
        if changes_detected:
            await self._save_schema_state(schema_state)

    async def _install_table(self, table_name: str, table_sql: str):
        """Install a table"""
        await self.db.execute(table_sql)
        log_info(f"Table {table_name} installed/updated successfully")

    async def _check_and_install_routines(self, schema_state: Dict, routine_dir: str, routine_type: str):
        """Check and install routines (procedures/functions) if there are changes"""
        routine_files = os.listdir(routine_dir)
        changes_detected = False
        
        for routine_file in routine_files:
            routine_path = os.path.join(routine_dir, routine_file)
            with open(routine_path, 'r') as f:
                routine_sql = f.read()
            routine_hash = hashlib.sha256(routine_sql.encode()).hexdigest()
            routine_name = os.path.splitext(routine_file)[0]
            
            if schema_state[routine_type].get(routine_name, {}).get("checksum") != routine_hash:
                await self._install_routine(routine_name, routine_sql, routine_type)
                schema_state[routine_type][routine_name] = {
                    "checksum": routine_hash,
                    "last_modified": self._get_utc_now()
                }
                schema_state["metadata"]["current_version"] += 1
                changes_detected = True
                self._changes_made = True
        
        if changes_detected:
            await self._save_schema_state(schema_state)

    async def _install_routine(self, routine_name: str, routine_sql: str, routine_type: str):
        """Install a routine (procedure/function)"""
        await self.db.execute(routine_sql)
        log_info(f"{routine_type.capitalize()} {routine_name} installed/updated successfully")

    async def _save_schema_state(self, schema_state: Dict):
        """Save the current schema state to the version file"""
        # Only update last_updated if changes were made
        if self._changes_made:
            schema_state["metadata"]["last_updated"] = self._get_utc_now()
        
        with open(self.version_file, 'w') as f:
            json.dump(schema_state, f, indent=4)
