from src.abstract_models.abstract_report import AbstractReport
from src.utils.format_reporting import FormatReporting
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException

"""
Ответ формирует набор данных в формате RTF
"""


class RTFReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.RTF

    def create(self, data: list):
        if not isinstance(data, list):
            raise ArgumentTypeException("data", "list")
        if len(data) == 0:
            raise EmptyException()
        self.result = r"{\rtf1\ansi\deff0"

        for row in data:
            self.result += r"\pard "
            self.serialize(self, row)
            self.result += r"\par "

        self.result += r"}"

    @staticmethod
    def serialize(self, data):
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(data.__class__, x)), dir(data)))
        for field in fields:
            value = getattr(data, field)
            if hasattr(value, '__dict__'):
                self.result += r"\b " + field + r":\b0 {\par "
                RTFReport.serialize(self, value)
                self.result += r"}\par "
            elif isinstance(value, list):
                self.result += r"\b " + field + r":\b0 " + ", "
                for val in value:
                    RTFReport.serialize(self, val)
                self.result += r"\par "
            else:
                self.result += r"\b " + field + r":\b0 " + str(value) + r"\par "

