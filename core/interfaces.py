from abc import ABC, abstractmethod

class IOutputStrategy(ABC):
    @abstractmethod
    def send(self, data: list):
        pass