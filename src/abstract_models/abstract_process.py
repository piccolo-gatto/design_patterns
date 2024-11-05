from abc import ABC, abstractmethod
from datetime import datetime
from src.utils.castom_exceptions import ArgumentTypeException

class AbstractProcess(ABC):
    __block_period: datetime = datetime.now()

    @property
    def block_period(self) -> datetime:
        return self.__block_period

    @block_period.setter
    def block_period(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("block_period", "str")

        self.__block_period = datetime.strptime(value, "%Y-%m-%d")

    @abstractmethod
    def process(self, transactions: list):
        pass