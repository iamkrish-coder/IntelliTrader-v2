# backend/services/BaseService.py
from fastapi import Depends
from abc import ABC, abstractmethod
from backend.database.database_manager import DatabaseManager
from backend.configurations.configuration import Configuration
from backend.modules.shared.shared_functions import SharedFunctions


class BaseService(ABC, SharedFunctions):
    def __init__(self, database: DatabaseManager = None):
        super().__init__()
        self.app_configuration = Configuration().read_app_configuration()
        self.table_configuration = Configuration().read_table_configuration()
        self.database = database or DatabaseManager.get_instance() 

