"""
Настройки
"""


class Settings:
    __organization_name = ""
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bic = ""
    __organization_type = ""

    @property
    def organization_name(self):
        return self.__organization_name

    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название должено быть передано в формате строки!")

        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise TypeError("ИНН должен быть передан в формате строки!")
        if len(value) != 12:
            raise ValueError("ИНН должен состоять из 12-ти символов!")

        self.__inn = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Счёт должен быть передан в формате строки!")
        if len(value) != 11:
            raise ValueError("Счёт должен состоять из 11-ти символов!")

        self.__account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Корреспондентский счёт должен быть передан в формате строки!")
        if len(value) != 11:
            raise ValueError("Корреспондентский счёт должен состоять из 11-ти символов!")

        self.__correspondent_account = value

    @property
    def bic(self):
        return self.__bic

    @bic.setter
    def bic(self, value: str):
        if not isinstance(value, str):
            raise TypeError("БИК должен быть передан в формате строки!")
        if len(value) != 9:
            raise ValueError("БИК должен состоять из 9-ти символов!")

        self.__bic = value

    @property
    def organization_type(self):
        return self.__organization_type

    @organization_type.setter
    def organization_type(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Вид собственности должен быть передан в формате строки!")
        if len(value) != 5:
            raise ValueError("Вид собственности должен состоять из 5-ти символов!")

        self.__organization_type = value