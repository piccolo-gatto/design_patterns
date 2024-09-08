from src.settings.settings import Settings
import os
import json
"""
Менеджер настроек
"""

class SettingsManager:
    __file_name = "settings.json"
    __settings: Settings = None

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

    def open(self, file_name: str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Имя файла долно быть передано в формате строки!")

        if file_name != "":
            self.__file_name = file_name

        try:
            full_name = os.path.relpath(self.__file_name)
            stream = open(full_name)
            data = json.load(stream)
            self.convert(data)

            return True
        except:
            self.__settings = self.__default_setting()
            return False

    """
    Перенос данных из словаря
    """

    def convert(self, dict: dict):
        if dict is None:
            raise AttributeError("Данные для заполнения отсутствуют!")
        for key, value in dict.items():
            if hasattr(self.__settings, key):
                setattr(self.__settings, key, value)

    """
    Загруженные настройки
    """

    @property
    def settings(self):
        return self.__settings

    """
    Набор настроек по умолчанию
    """

    def __default_setting(self):
        data = Settings()
        data.inn = "380080920202"
        data.organization_name = "Рога и копыта (default)"
        data.account = "12345678900"
        data.correspondent_account = "12345678900"
        data.bic = "044525225"
        data.organization_type = "11111"

        return data