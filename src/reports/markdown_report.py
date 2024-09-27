from src.utils.format_reporting import FormatReporting
from src.abstract_models.abstract_report import AbstractReport
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException

"""
Ответ формирует набор данных в формате Markdown
"""


class MDReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.MARKDOWN

    def create(self, data: list):
        if not isinstance(data, list):
            raise ArgumentTypeException("data", "list")
        if len(data) == 0:
            raise EmptyException()

        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model)))

        line = ""
        for field in fields:
            self.result += f"|{str(field)}"
            line += "|---"
        self.result += "|\n" + line + "|\n"

        for row in data:
            for field in fields:
                value = getattr(row, field)
                self.result += f"|{str(value)}"
            self.result += "|\n"