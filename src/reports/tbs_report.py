import json
from src.utils.format_reporting import FormatReporting
from src.abstract_models.abstract_report import AbstractReport
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException


class TBSReport(AbstractReport):

    def __init__(self) -> None:
        super().__init__()
        self.__format = FormatReporting.TBS


    def create(self, data: list):
        if len(data) == 0:
            raise  EmptyException()
        report = []
        for turnover_before, turnover_between in zip(data[0], data[1]):
            report_entry = {
                "warehouse": turnover_before.warehouse.name,
                "nomenclature": turnover_before.nomenclature.name,
                "range": turnover_before.measurement.name,
                "start_balance": turnover_before.turnover,
                "period_balance": turnover_between.turnover,
                "end_balance": turnover_before.turnover + turnover_between.turnover
            }
            report.append(report_entry)
        self.result = json.dumps(report, ensure_ascii=False, indent=2)


