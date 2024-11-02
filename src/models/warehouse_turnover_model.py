from src.models.nomenclature_model import NomenclatureModel
from src.models.measurement_model import MeasurementModel
from src.models.warehouse_model import WarehouseModel
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException


class WarehouseTurnoverModel(AbstractReference):
    __warehouse: WarehouseModel = None
    __nomenclature: NomenclatureModel = None
    __turnover: int = 0
    __measurement: MeasurementModel = None

    @property
    def warehouse(self) -> WarehouseModel:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: WarehouseModel):
        if not isinstance(value, WarehouseModel):
            raise ArgumentTypeException("warehouse", "WarehouseModel")

        self.__warehouse = value

    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        if not isinstance(value, NomenclatureModel):
            raise ArgumentTypeException("nomenclature", "NomenclatureModel")

        self.__nomenclature = value

    @property
    def turnover(self) -> int:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: int):
        if not isinstance(value, int):
            raise ArgumentTypeException("turnover", "int")

        self.__turnover = value

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
