from src.abstract_models.abstract_logic import AbstractLogic
from src.abstract_models.abstract_report import AbstractReport
from src.utils.format_reporting import FormatReporting
from src.utils.settings_manager import SettingsManager
from src.models.settings_model import SettingsModel
from src.utils.castom_exceptions import ArgumentTypeException, UnknownValueException


"""
Фабрика для формирования отчетов
"""


class ReportFactory(AbstractLogic):
    __reports: dict = {}
    __settings_manager: SettingsManager = None

    def __init__(self, manager: SettingsManager) -> None:
        super().__init__()
        self.__settings_manager = manager
        # Наборы отчетов
        for key, value in manager.settings.report_formats.items():
            for cls in AbstractReport.__subclasses__():
                if value == cls.__name__:
                    self.__reports[key] = cls

    @property
    def reports(self) -> dict:
        return self.__reports

    @reports.setter
    def reports(self, value: dict):
        if not isinstance(value, dict):
            raise ArgumentTypeException("value", "dict")

        self.__reports = value

    @property
    def settings(self) -> SettingsModel:
        return self.__settings_manager.settings


    """
    Получить инстанс нужного отчета
    """

    def create(self, format: FormatReporting) -> AbstractReport:
        if not isinstance(format, FormatReporting):
            raise ArgumentTypeException("format", "FormatReporting")

        if format.name not in self.__reports.keys():
            raise UnknownValueException()

        report_name = self.__reports[format.name]

        return report_name()

    def get_formats(self):
        for key, value in self.__settings_manager.settings.report_formats.items():
            self.reports[FormatReporting[key]] = value

    def create_default(self):
        return self.create(self.settings.report)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
