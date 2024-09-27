from abc import ABC, abstractmethod
from src.utils.format_reporting import FormatReporting
#from Src.Core.validator import validator

"""
Абстрактный класс для наследования для отчетов
"""


class AbstractReport(ABC):
    __format: FormatReporting = FormatReporting.CSV
    __result: str = ""

    """
    Сформировать
    """

    @abstractmethod
    def create(self, data: list):
        pass

    """
    Тип формата
    """

    @property
    def format(self) -> FormatReporting:
        return self.__format

    """
    Результат формирования отчета
    """

    @property
    def result(self) -> str:
        return self.__result

    @result.setter
    def result(self, value: str):
        #validator.validate(value, str)
        self.__result = value