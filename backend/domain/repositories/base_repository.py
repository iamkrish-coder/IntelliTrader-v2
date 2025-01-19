from typing import Optional, Dict, List, Any
import asyncpg
from backend.core.exceptions import ApiException
from backend.database.managers.database_manager import DatabaseManager
from backend.domain.schemas.base_schema import BaseResponse

class BaseRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def execute_procedure(
        self,
        procedure_name: str,
        *args: Any,
        transaction: bool = False
    ) -> Dict[str, Any]:
        """Execute a stored procedure"""
        output_params = BaseResponse()
        args_with_output = list(args) + [
            output_params.status, 
            output_params.data
        ]
        
        return await self.db_manager.call_procedure(
            procedure_name, 
            *args_with_output,
            transaction=transaction
        )

    async def execute_function(
        self,
        function_name: str,
        *args: Any,
        fetch_mode: str = 'one',
        transaction: bool = False
    ) -> Dict[str, Any]:
        """Execute a database function"""
        return await self.db_manager.call_function(
            function_name, 
            *args, 
            fetch_mode=fetch_mode,
            transaction=transaction
        )
