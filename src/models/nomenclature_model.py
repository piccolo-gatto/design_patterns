from src.abstract_models.abstract_reference import AbstractReference
from src.models.measurement_model import MeasurementModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils.castom_exceptions import ArgumentMaxLengthException, ArgumentTypeException


class NomenclatureModel(AbstractReference):
    __name: str = ""
    __full_name: str = ""
    __group: NomenclatureGroupModel = None
    __measurement: MeasurementModel = None

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("name", "str")
        if len(value) > 50:
            raise ArgumentMaxLengthException("name", 50)

        self.__name = value

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("full_name", "str")
        if len(value) > 255:
            raise ArgumentMaxLengthException("full_name", 255)

        self.__full_name = value

    @property
    def measurement(self) -> MeasurementModel:
        return self.__measurement

    @measurement.setter
    def measurement(self, value: MeasurementModel):
        if not isinstance(value, MeasurementModel):
            raise ArgumentTypeException("measurement", "MeasurementModel")

        self.__measurement = value

    @property
    def group(self) -> NomenclatureGroupModel:
        return self.__group

    @group.setter
    def group(self, value: NomenclatureGroupModel):
        if not isinstance(value, NomenclatureGroupModel):
            raise ArgumentTypeException("group", "NomenclatureGroupModel")

        self.__group = value


    def set_compare_mode(self, other_object) -> bool:
        if other_object is None: return False
        if not isinstance(other_object, AbstractReference): return False

        return self.__name == other_object.name
