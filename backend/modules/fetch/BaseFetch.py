# IntelliTrader\backend\modules\fetch\BaseFetch.py

from abc import ABC, abstractmethod
from ..shared.shared_functions import SharedFunctions
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class BaseFetch(ABC, SharedFunctions):
    def __init__(self, modules, database):
        super().__init__(self, modules)
        self.modules = modules
        self.database = database

