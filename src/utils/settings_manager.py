import os
import json
from src.models.settings_model import SettingsModel
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException

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

        return data

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
