import json
from src.utils.format_reporting import FormatReporting
from src.abstract_models.abstract_report import AbstractReport
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException
from datetime import datetime
"""
Ответ формирует набор данных в формате Json
"""


class JSONReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.JSON

        

    def create(self, data: list):
        if not isinstance(data, list):
            raise ArgumentTypeException("data", "list")
        if len(data) == 0:
            raise EmptyException()
        report = []
        for row in data:
            report.append(self.serialize(row))
        self.result = json.dumps(report, ensure_ascii=False, indent=2)
    @staticmethod
    def serialize(data) -> dict:
        row_data = {}
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(data.__class__, x)), dir(data)))
        for field in fields:
            value = getattr(data, field)
            if hasattr(value, '__dict__'):
                row_data[field] = JSONReport.serialize(value)
            elif isinstance(value, list):
                row_data[field] = []
                for val in value:
                    row_data[field].append(JSONReport.serialize(val))
            else:
                if type(value) == datetime:
                    value = str(value)
                row_data[field] = value
        return row_data
