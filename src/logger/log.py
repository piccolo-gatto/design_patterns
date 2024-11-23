from src.logger.log_type import LogType
from src.utils.castom_exceptions import ArgumentTypeException


class Log():
    __type: LogType = LogType.INFO
    __message: str = ""

    def __init__(self, type: LogType = LogType.INFO, message: str = ""):
        self.__type = type
        self.__message = message

    @property
    def type(self) -> LogType:
        return self.__type

    @type.setter
    def type(self, value: LogType):
        if not isinstance(value, LogType):
            ArgumentTypeException('type', "LogType")
        self.__type = value

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        if not isinstance(value, str):
            ArgumentTypeException('message', "str")
        self.__message = value