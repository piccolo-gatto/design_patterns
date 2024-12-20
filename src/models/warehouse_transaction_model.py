from datetime import datetime
from src.models.nomenclature_model import NomenclatureModel
from src.models.measurement_model import MeasurementModel
from src.models.warehouse_model import WarehouseModel
from src.models.transaction_type import TransactionType
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException


class WarehouseTransactionModel(AbstractReference):
    __warehouse: WarehouseModel = None
    __nomenclature: NomenclatureModel = None
    __count: int = 0
    __type: str = TransactionType.RECEIPT.value
    __measurement: MeasurementModel = None
    __date: datetime = datetime.now().isoformat()

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
    def count(self) -> int:
        return self.__count

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise ArgumentTypeException("count", "int")

        self.__count = value

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("type", "str")
        self.__type = value

    @property
    def measurement(self) -> MeasurementModel:
        return self.__measurement

    @measurement.setter
    def measurement(self, value: MeasurementModel):
        if not isinstance(value, MeasurementModel):
            raise ArgumentTypeException("measurement", "MeasurementModel")

        self.__measurement = value

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("date", "str")

        self.__date = datetime.strptime(value, "%Y-%m-%d")

    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)
