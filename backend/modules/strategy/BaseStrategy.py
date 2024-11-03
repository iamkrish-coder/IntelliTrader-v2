# IntelliTrader\backend\modules\strategy\BaseStrategy.py

from abc import abstractmethod
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class BaseStrategy:
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self):
        raise NotImplementedError("Subclasses must implement this method")
