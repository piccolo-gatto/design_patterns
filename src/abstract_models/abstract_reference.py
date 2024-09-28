from abc import ABC, abstractmethod
import uuid

from src.utils.castom_exceptions import ArgumentTypeException, ArgumentMaxLengthException

"""
Абстрактный класс для наследования моделей данных
"""


class AbstractReference(ABC):
    __unique_code: str = uuid.uuid1().hex
    __name = ""

    """
    Уникальный код
    """

    @property
    def unique_code(self) -> str:
        return self.__unique_code

    """
    Вариант сравнения (по коду)
    """

    @abstractmethod
    def set_compare_mode(self, other_object) -> bool:
        if other_object is None: return False
        if not isinstance(other_object, AbstractReference): return False

        return self.__unique_code == other_object.unique_code

    def __eq__(self, value: object) -> bool:
        return self.set_compare_mode(value)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("name", "str")
        if len(value) > 50:
            raise ArgumentMaxLengthException("name", 50)

        self.__name = value
