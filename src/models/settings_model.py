from datetime import datetime, date
from src.utils.castom_exceptions import ArgumentLengthException, UnknownValueException, ArgumentTypeException
from src.utils.format_reporting import FormatReporting
from src.logger.log_type import LogType
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType

"""
Настройки
"""


class SettingsModel(AbstractReference):
    __organization_name: str = ""
    __inn: str = ""
    __account: str = ""
    __correspondent_account: str = ""
    __bic: str = ""
    __organization_type: str = ""
    __report: str = "JSONReport"
    __report_formats = {}
    __block_period: datetime = date.today().isoformat()
    __first_start: bool = True
    __min_log_type: LogType = LogType.DEBUG
    __log_to_console: bool = True
    __log_to_file: bool = True
    __log_file_path: str = "../log.txt"


    @property
    def organization_name(self) -> str:
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("organization_name", "str"))
            raise ArgumentTypeException("organization_name", "str")
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Имя организации {value}")
        self.__organization_name = value

    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("inn", "str"))
            raise ArgumentTypeException("inn", "str")
        if len(value) != 12:
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentLengthException("inn", 12))
            raise ArgumentLengthException("inn", 12)
        ObserveService.raise_event(EventType.DEBUG_LOG, f"ИНН {value}")
        self.__inn = value

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("account", "str"))
            raise ArgumentTypeException("account", "str")
        if len(value) != 11:
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentLengthException("account", 11))
            raise ArgumentLengthException("account", 11)
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Адрес {value}")
        self.__account = value

    @property
    def correspondent_account(self) -> str:
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("correspondent_account", "str"))
            raise ArgumentTypeException("correspondent_account", "str")
        if len(value) != 11:
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentLengthException("correspondent_account", 11))
            raise ArgumentLengthException("correspondent_account", 11)

        ObserveService.raise_event(EventType.DEBUG_LOG, f"Адрес для корреспонденции {value}")
        self.__correspondent_account = value

    @property
    def bic(self) -> str:
        return self.__bic

    @bic.setter
    def bic(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("bic", "str"))
            raise ArgumentTypeException("bic", "str")
        if len(value) != 9:
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentLengthException("bic", 9))
            raise ArgumentLengthException("bic", 9)
        ObserveService.raise_event(EventType.DEBUG_LOG, f"БИК {value}")
        self.__bic = value

    @property
    def organization_type(self) -> str:
        return self.__organization_type

    @organization_type.setter
    def organization_type(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("organization_type", "str"))
            raise ArgumentTypeException("organization_type", "str")
        if len(value) != 5:
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentLengthException("organization_type", 5))
            raise ArgumentLengthException("organization_type", 5)
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Тип организации {value}")
        self.__organization_type = value

    @property
    def report(self):
        return self.__report

    @report.setter
    def report(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("report", "str"))
            raise ArgumentTypeException("report", "str")
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Отчёт по умолчанию {value}")
        self.__report = value

    @property
    def report_formats(self):
        return self.__report_formats

    @report_formats.setter
    def report_formats(self, value: dict):
        if not isinstance(value, dict):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("value", "dict"))
            raise ArgumentTypeException("value", "dict")
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Список доступных отчётов {value}")
        self.__report_formats = value

    @property
    def block_period(self) -> datetime:
        return self.__block_period

    @block_period.setter
    def block_period(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("block_period", "str"))
            raise ArgumentTypeException("block_period", "str")
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Дата блокировки {value}")
        self.__block_period = datetime.strptime(value, "%Y-%m-%d")

    @property
    def first_start(self):
        return self.__first_start

    @first_start.setter
    def first_start(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("first_start", "str"))
            raise ArgumentTypeException("first_start", "str")
        if value == "True":
            ObserveService.raise_event(EventType.DEBUG_LOG,f"Это первый старт проекта")
            self.__log_to_file = True
        elif value == "False":
            ObserveService.raise_event(EventType.DEBUG_LOG,f"Это не первый старт проекта")
            self.__log_to_file = False
        else:
            ObserveService.raise_event(EventType.ERROR_LOG, "Неизвестные данные для first_start")

    @property
    def min_log_type(self) -> LogType:
        return self.__min_log_type

    @min_log_type.setter
    def min_log_type(self, value: int):
        if not isinstance(value, int):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException('min_log_type', "int"))
            ArgumentTypeException('min_log_type', "int")
        for type in LogType:
            if type.value == value:
                ObserveService.raise_event(EventType.DEBUG_LOG, f"Минимальный уровень логирования {type.value} ({type.name})")
                self.__min_log_type = type

    @property
    def log_to_console(self):
        return self.__log_to_console

    @log_to_console.setter
    def log_to_console(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException('log_to_console', "str"))
            raise ArgumentTypeException("log_to_console", "str")
        if value == "True":
            ObserveService.raise_event(EventType.DEBUG_LOG,f"Логирование в консоль разешено")
            self.__log_to_console = True
        elif value == "False":
            ObserveService.raise_event(EventType.DEBUG_LOG,f"Логирование в консоль запрещено")
            self.__log_to_console = False
        else:
            ObserveService.raise_event(EventType.ERROR_LOG, "Неизвестные данные для log_to_console")
            raise UnknownValueException()


    @property
    def log_to_file(self):
        return self.__log_to_file

    @log_to_file.setter
    def log_to_file(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException('log_to_file', "str"))
            raise ArgumentTypeException("log_to_file", "str")
        if value == "True":
            ObserveService.raise_event(EventType.DEBUG_LOG,f"Логирование в файл разешено")
            self.__log_to_file = True
        elif value == "False":
            ObserveService.raise_event(EventType.DEBUG_LOG,f"Логирование в файл запрещено")
            self.__log_to_file = False
        else:
            ObserveService.raise_event(EventType.ERROR_LOG, "Неизвестные данные для log_to_file")
            raise UnknownValueException()
    @property
    def log_file_path(self) -> str:
        return self.__log_file_path

    @log_file_path.setter
    def log_file_path(self, value: str):
        if not isinstance(value, str):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException('log_file_path', "str"))
            ArgumentTypeException('log_file_path', "str")
        ObserveService.raise_event(EventType.DEBUG_LOG, f"Путь до файла логирования {value}")
        self.__log_file_path = value

    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)