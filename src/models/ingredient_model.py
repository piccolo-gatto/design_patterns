from src.abstract_models.abstract_reference import AbstractReference
from src.models.nomenclature_model import NomenclatureModel
from src.models.measurement_model import MeasurementModel
from src.utils.castom_exceptions import ArgumentMaxLengthException, ArgumentTypeException


class IngredientModel(AbstractReference):
    __count: int = 0
    __nomenclature: NomenclatureModel = None
    __measurement: MeasurementModel = None

    @property
    def count(self) -> int:
        return self.__count

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise ArgumentTypeException("count", "int")

        self.__count = value

    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        if not isinstance(value, NomenclatureModel):
            raise ArgumentTypeException("nomenclature", "NomenclatureModel")

        self.__nomenclature = value

    @property
    def measurement(self) -> MeasurementModel:
        return self.__measurement

    @measurement.setter
    def measurement(self, value: MeasurementModel):
        if not isinstance(value, MeasurementModel):
            raise ArgumentTypeException("measurement", "MeasurementModel")

        self.__measurement = value


    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)