import uuid
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException


class MeasurementModel(AbstractReference):
    __name: str = ""
    __coefficient: int = 1
    __base: 'MeasurementModel' = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("name", "str")

        self.__name = value

    @property
    def base(self) -> 'MeasurementModel':
        return self.__base

    @base.setter
    def base(self, base: 'MeasurementModel'):
        if not isinstance(base, MeasurementModel):
            raise ArgumentTypeException("base", "MeasurementModel")

        self.__base = base

    @property
    def coefficient(self) -> int:
        return self.__coefficient

    @coefficient.setter
    def coefficient(self, value: int):
        if not isinstance(value, int):
            raise ArgumentTypeException("coefficient", "int")

        self.__coefficient = value

    @staticmethod
    def default_group_gram():
        item = MeasurementModel()
        item.unique_code = uuid.uuid1().hex
        item.name = "гр"
        return item

    @staticmethod
    def default_group_piece():
        item = MeasurementModel()
        item.unique_code = uuid.uuid1().hex
        item.name = "шт"
        return item

    @staticmethod
    def default_group_milliliter():
        item = MeasurementModel()
        item.unique_code = uuid.uuid1().hex
        item.name = "мл"
        return item


    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)
