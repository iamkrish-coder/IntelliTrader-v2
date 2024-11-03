from abc import ABC, abstractmethod


class BaseSnsManager(ABC):

    @abstractmethod
    def execute(self):
        pass
