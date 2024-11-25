from src.logger.log_type import LogType
from src.logger.log import Log
from src.utils.event_type import EventType
from src.utils.settings_manager import SettingsManager
from datetime import datetime
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.observe_service import ObserveService



class Logger(AbstractLogic):
    __min_type: LogType
    __file_path: str
    __log_to_console: bool
    __log_to_file: bool

    def __init__(self, settings: SettingsManager):
        self.__min_type = settings.settings.min_log_type
        self.__file_path = settings.settings.log_file_path
        self.__log_to_console = settings.settings.log_to_console
        self.__log_to_file = settings.settings.log_to_file
        ObserveService.append(self)

    def log(self, log: Log):
        log_str = f"{datetime.now().isoformat()}\t[{log.type.name}] {log.message}\n"
        if self.__log_to_file:
            with open(self.__file_path, "a", encoding="utf-8") as f:
                f.write(log_str)
        if self.__log_to_console:
            print(log_str)

    def info(self, message: str):
        log = Log(LogType.INFO, message)
        self.log(log)

    def error(self, message: str):
        log = Log(LogType.ERROR, message)
        self.log(log)

    def debug(self, message: str):
        log = Log(LogType.DEBUG, message)
        self.log(log)

    def handle_event(self, type: EventType, params):
        if type == EventType.INFO_LOG and self.__min_type.value >= LogType.INFO.value:
            self.info(params)
        if type == EventType.ERROR_LOG and self.__min_type.value >= LogType.ERROR.value:
            self.error(params)
        if type == EventType.DEBUG_LOG and self.__min_type.value >= LogType.DEBUG.value:
            self.debug(params)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)