import os
import json
import hashlib
from typing import List, Any
from backend.utils.logging_utils import *

class DatabaseUpgrade:
    def __init__(self, asyncpg_connection, db_updates_dir, db_routines_dir):
        self.asyncpg_connection = asyncpg_connection
        self.db_updates_dir = db_updates_dir
        self.db_routines_dir = db_routines_dir

    async def check_for_updates(self) -> List[Any]:
        """Executes all stored procedures and functions found in the backend.database.routines directory only if changes are detected."""

        # Load previously executed hashes from the file
        executed_hashes = {}
        if not os.path.exists(self.db_updates_dir):
            os.makedirs(self.db_updates_dir)

        checksum_file = os.path.join(self.db_updates_dir, 'update_checksum.json')
        if os.path.exists(checksum_file):
            with open(checksum_file, 'r') as hash_file:
                executed_hashes = json.load(hash_file)

        # Track if any changes were made
        database_updated = False

        # Check for updates
        for module_name in os.listdir(self.db_routines_dir):
            module_path = os.path.join(self.db_routines_dir, module_name)
            if os.path.isdir(module_path):
                for filename in os.listdir(module_path):
                    file_path = os.path.join(module_path, filename)
                    if filename.endswith('.sql'):
                        routine = filename.replace('.sql', '')
                        last_modified_time = os.path.getmtime(file_path)

                        # Check if the file has been modified
                        if (filename not in executed_hashes or 
                            executed_hashes[filename]['last_modified_time'] != last_modified_time):
                            
                            # Calculate the hash of the SQL command only if modified
                            with open(file_path, 'r') as file:
                                sql_command = file.read()
                            command_hash = hashlib.sha256(sql_command.encode()).hexdigest()

                            # Check if the checksum has changed
                            if (filename not in executed_hashes or 
                                executed_hashes[filename]['checksum'] != command_hash):
                                try:
                                    # Log the SQL command for debugging
                                    log_info(f"Creating routine: {routine}")
                                    await self.asyncpg_connection.execute(sql_command)

                                    # Update the executed_hashes with new values
                                    executed_hashes[filename] = {
                                        'last_modified_time': last_modified_time,
                                        'checksum': command_hash
                                    }
                                    database_updated = True  # Mark that changes were made
                                except Exception as error:
                                    log_error(f"Error executing {file_path}: {error}")
                        else:
                            log_info(f"No changes detected for {filename}")

        # Save the updated hashes back to the file only if changes were made
        if database_updated:
            with open(checksum_file, 'w') as file:
                json.dump(executed_hashes, file) 
        else:
            log_info("Database is up to date.")