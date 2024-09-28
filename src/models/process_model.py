from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException


class ProcessModel(AbstractReference):
    __name: str = ""
    __content: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("name", "str")

        self.__name = value


    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("content", "str")

        self.__content = value

    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)