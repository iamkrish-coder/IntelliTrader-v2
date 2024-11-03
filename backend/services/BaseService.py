# backend/controllers/BaseService.py

from abc import ABC, abstractmethod
from backend.configurations.configuration import Configuration
from backend.controllers.database_controller import DatabaseController
from backend.modules.shared.shared_functions import SharedFunctions
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class BaseService(ABC, SharedFunctions):
    def __init__(self):
        super().__init__()
        self.app_configuration = Configuration().read_app_configuration()
        self.table_configuration = Configuration().read_table_configuration()
        self.database = DatabaseController(self.table_configuration)

    def prepare_request_parameters(self, event, table, model, dataset, projection=[], filters={}):
        attributes = None
        config = self.database.table_configuration[table]
        if model:
            attributes = model(**dataset).convert_table_rows_to_dict(config)
        return {
            "event": event,
            "table": table,
            "config": config,
            "data": {
                "attributes": attributes,
                "projection": projection,
                "filters": filters,
            },
        }

    def database_request(self, request):
        log_info(f"Requesting AWS DynamoDB...")
        return self.database.manage_table_records(request)
