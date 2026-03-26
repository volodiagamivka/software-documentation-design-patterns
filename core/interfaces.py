from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def save_batch(self, users, games, sessions): pass

class ICSVDataSource(ABC):
    @abstractmethod
    def get_data(self, path): pass