from abc import ABC, abstractmethod
from src.utils.castom_exceptions import ArgumentTypeException


class AbstractPrototype(ABC):
    __data = []

    def __init__(self, source:list) -> None:
        super().__init__()
        if not isinstance(source, list):
            ArgumentTypeException('sourse', "list")
        self.__data = source

    @abstractmethod
    def create(self, data:list, filter):
        if not isinstance(data, list):
            ArgumentTypeException('data', "list")

    @property
    def data(self) -> list:
        return self.__data    
    
    @data.setter
    def data(self, value:list):
        self.__data = value
