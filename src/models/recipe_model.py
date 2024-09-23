import re
from src.models.nomenclature_model import NomenclatureModel
from src.models.measurement_model import MeasurementModel
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException


class RecipeModel(AbstractReference):
    __name: str = ""
    __count: int = 0
    __minutes: int = 0
    __ingredients: list = []
    __process: list = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("name", "str")

        self.__name = value

    @property
    def count(self) -> int:
        return self.__count

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise ArgumentTypeException("count", "int")

        self.__count = value

    @property
    def minutes(self) -> int:
        return self.__minutes

    @minutes.setter
    def minutes(self, value: int):
        if not isinstance(value, int):
            raise ArgumentTypeException("minutes", "int")

        self.__minutes = value

    @property
    def ingredients(self) -> list:
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: list):
        if not isinstance(value, list):
            raise ArgumentTypeException("ingredients", "list")

        self.__ingredients = value

    @property
    def process(self) -> list:
        return self.__process

    @process.setter
    def process(self, value: list):
        if not isinstance(value, list):
            raise ArgumentTypeException("process", "list")

        self.__process = value


    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)
