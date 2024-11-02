from abc import ABC, abstractmethod

class AbstractProcess(ABC):

    @abstractmethod
    def process(self, transactions: list) -> list:
        pass