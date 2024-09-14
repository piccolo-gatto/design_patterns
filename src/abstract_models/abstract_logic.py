from abc import ABC, abstractmethod

"""
Абстрактный класс для обработки логики
"""


class AbstractLogic(ABC):
    __error_text: str = ""

    @property
    def error_text(self) -> str:
        return self.__error_text.strip()

    @error_text.setter
    def error_text(self, message: str):
        self.__error_text = message.strip()

    @property
    def is_error(self) -> bool:
        return self.error_text != ""

    def _inner_set_exception(self, ex: Exception):
        self.__error_text = f"Ошибка! Исключение {ex}"

    """
    Абстрактный метод для загрузки и обработки исключений
    """

    @abstractmethod
    def set_exception(self, ex: Exception):
        pass
