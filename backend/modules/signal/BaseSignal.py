# IntelliTrader\backend\modules\signal\BaseSignal.py

from abc import abstractmethod
from sys import modules
from backend.constants.const import *
from backend.enumerations.enums import *
from backend.utils.logging_utils import *


class BaseSignal:
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self):
        raise NotImplementedError("Subclasses must implement this method")
