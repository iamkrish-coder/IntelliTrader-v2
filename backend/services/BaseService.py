# backend/services/BaseService.py
from fastapi import Depends
from abc import ABC, abstractmethod
from backend.database.database import Database
from backend.configurations.configuration import Configuration
from backend.modules.shared.shared_functions import SharedFunctions
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class BaseService(ABC, SharedFunctions):
    def __init__(self, database: Database = None):
        super().__init__()
        self.app_configuration = Configuration().read_app_configuration()
        self.table_configuration = Configuration().read_table_configuration()
        self.database = database or Database.get_instance() 

