from src.dto.filter import FilterDTO
from datetime import datetime, date
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.castom_exceptions import ArgumentTypeException

class TransactionFilterDTO(AbstractLogic):
    __nomenclature: FilterDTO
    __warehouse: FilterDTO
    __start_period: datetime
    __end_period: datetime

    @property
    def warehouse(self) -> FilterDTO:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: FilterDTO):
        if not isinstance(value, FilterDTO):
            ArgumentTypeException('warehouse', "FilterDTO")
        self.__warehouse = value

    @property
    def nomenclature(self) -> FilterDTO:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: FilterDTO):
        if not isinstance(value, FilterDTO):
            ArgumentTypeException('nomenclature', "FilterDTO")
        self.__nomenclature = value

    @property
    def start_period(self) -> datetime:
        return self.__start_period

    @start_period.setter
    def start_period(self, value: datetime):
        self.__start_period = value

    @property
    def end_period(self) -> datetime:
        return self.__end_period

    @end_period.setter
    def end_period(self, value: datetime):
        self.__end_period = value


    def from_dict(self, data: dict):
        try:
            filter = TransactionFilterDTO()
            warehouse_filter = data['warehouse']
            nomenclature_filter = data['nomenclature']
            filter.start_period = datetime.strptime(data["start_period"], "%Y-%m-%d")
            filter.end_period = datetime.strptime(data["end_period"], "%Y-%m-%d")


            filter.warehouse = FilterDTO().from_dict(warehouse_filter)
            filter.nomenclature = FilterDTO().from_dict(nomenclature_filter)

            return filter
        except Exception as e:
            raise e

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
