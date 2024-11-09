import os
import json
from src.reports.markdown_report import MDReport
from src.reports.csv_report import CSVReport
from src.reports.json_report import JSONReport
from src.reports.xml_report import XMLReport
from src.reports.rtf_report import RTFReport
from src.models.settings_model import SettingsModel
from src.utils.format_reporting import FormatReporting
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException, UnknownValueException
from src.utils.event_type import EventType

"""
Менеджер настроек
"""


class SettingsManager(AbstractLogic):
    __file_name: str = "settings.json"
    __settings: SettingsModel = None


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting()

    """
    Открыть и загрузить настройки
    """

    def open(self, file_name: str = "") -> bool:
        if not isinstance(file_name, str):
            raise ArgumentTypeException("file_name", "str")

        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = os.path.relpath(self.__file_name)
            stream = open(full_name)
            data = json.load(stream)
            self.convert(data)

            return True
        except Exception as ex:
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False

    """
    Перенос данных из словаря
    """

    def convert(self, dict: dict):
        if dict is None:
            raise EmptyException()
        for key, value in dict.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    """
    Загруженные настройки
    """

    @property
    def settings(self) -> SettingsModel:
        return self.__settings


    """
    Набор настроек по умолчанию
    """

    def __default_setting(self) -> SettingsModel:
        data = SettingsModel()
        data.inn = "380080920202"
        data.organization_name = "Рога и копыта (default)"
        data.account = "12345678900"
        data.correspondent_account = "12345678900"
        data.bic = "044525225"
        data.organization_type = "11111"
        data.report = "JSON"
        data.report_formats = {
        "CSV": "CSVReport",
        "MARKDOWN": "MDReport",
        "JSON": "JSONReport"
    }

        return data

    def report_type(self, format: FormatReporting = None):
        if isinstance(format, FormatReporting):
            raise ArgumentTypeException("format", "FormatReporting")

        if format is None:
            format = self.__settings.report
        try:
            report_class = self.settings.report_formats.get(format.name, None)
            return report_class()

        except:
            raise UnknownValueException()

    def format_report(self) -> str:
        report = JSONReport()
        print(self.settings)
        report.create([self.settings])
        return report.result

    def save(self):
        report = self.format_report()
        with open("data/settings.json", "w", encoding="utf-8") as f:
            f.write(report)
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)