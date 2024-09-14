from src.abstract_models.abstract_reference import AbstractReference
from src.utils.settings_manager import SettingsManager
from src.utils.castom_exceptions import ArgumentTypeException, ArgumentLengthException


class OrganizationModel(AbstractReference):
    __inn: str = ""
    __bic: str = ""
    __account: str = ""
    __organization_type: str = ""

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

    def load_settings(self, value: SettingsManager):
        if not isinstance(value, SettingsManager):
            raise TypeError("")

        self.__inn = value.settings.inn
        self.__bic = value.settings.bic
        self.__account = value.settings.account
        self.__organization_type = value.settings.organization_type

    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)
