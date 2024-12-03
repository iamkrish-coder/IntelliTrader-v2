from typing import Any, Dict, Optional
from backend.core.exceptions import ApiException
from backend.database.database_manager import DatabaseManager

class BaseRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    async def execute_stored_procedure(
        self, 
        procedure_name: str, 
        *args: Any
    ) -> Dict[str, Any]:
        """
        Execute a stored procedure with proper async context management.
        
        Args:
            procedure_name: Name of the stored procedure
            *args: Arguments to pass to the stored procedure
            
        Returns:
            Dict containing the result of the stored procedure
        """
        try:
            async with self.db.connection() as conn:
                result = await conn.execute_stored_procedure(
                    procedure_name,
                    *args
                )
                return {"success": True, "data": result}
        except Exception as error:
            raise ApiException.internal_server_error(
                message="DATABASE_OPERATION_FAILED",
                data=str(error)
            )
