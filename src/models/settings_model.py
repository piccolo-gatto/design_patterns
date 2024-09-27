from src.utils.castom_exceptions import ArgumentLengthException, UnknownValueException, ArgumentTypeException
from src.utils.format_reporting import FormatReporting

"""
Настройки
"""


class SettingsModel:
    __organization_name: str = ""
    __inn: str = ""
    __account: str = ""
    __correspondent_account: str = ""
    __bic: str = ""
    __organization_type: str = ""
    __report: FormatReporting = FormatReporting.CSV

    @property
    def organization_name(self) -> str:
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("organization_name", "str")

        self.__organization_name = value

    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("inn", "str")
        if len(value) != 12:
            raise ArgumentLengthException("inn", 12)

        self.__inn = value

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("account", "str")
        if len(value) != 11:
            raise ArgumentLengthException("account", 11)

        self.__account = value

    @property
    def correspondent_account(self) -> str:
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("correspondent_account", "str")
        if len(value) != 11:
            raise ArgumentLengthException("correspondent_account", 11)

        self.__correspondent_account = value

    @property
    def bic(self) -> str:
        return self.__bic

    @bic.setter
    def bic(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("bic", "str")
        if len(value) != 9:
            raise ArgumentLengthException("bic", 9)

        self.__bic = value

    @property
    def organization_type(self) -> str:
        return self.__organization_type

    @organization_type.setter
    def organization_type(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("organization_type", "str")
        if len(value) != 5:
            raise ArgumentLengthException("organization_type", 5)

        self.__organization_type = value

    @property
    def report(self):
        return self.__report

    @report.setter
    def report(self, value: FormatReporting):
        if not isinstance(value, FormatReporting):
            raise ArgumentTypeException("value", "FormatReporting")
        self.__report = value
