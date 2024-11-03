from abc import ABC, abstractmethod


class BaseSqsManager(ABC):

    @abstractmethod
    def execute(self):
        pass
