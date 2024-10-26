from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.dto.transaction_filter import TransactionFilterDTO
from src.dto.filter import FilterDTO
from src.abstract_models.abstract_prototype import AbstractPrototype
from src.logics.domain_prototype import DomainPrototype
from src.dto.filter_logic import FilterLogic
from datetime import datetime
from src.utils.castom_exceptions import ArgumentTypeException


class TransactionPrototype(DomainPrototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, TransactionFilterDTO: TransactionFilterDTO):
        self.data = data
        if TransactionFilterDTO.warehouse:
            self.data = self.filter_id(self.data, TransactionFilterDTO.warehouse)
            self.data = self.filter_name(self.data, TransactionFilterDTO.warehouse)
        if TransactionFilterDTO.nomenclature:
            self.data = self.filter_id(self.data, TransactionFilterDTO.nomenclature)
            self.data = self.filter_name(self.data, TransactionFilterDTO.nomenclature)

        if TransactionFilterDTO.start_period and TransactionFilterDTO.end_period:
            self.data = self.filter_period(self.data, TransactionFilterDTO.start_period, TransactionFilterDTO.end_period)

        return TransactionPrototype(data)

    def filter_id(self, data: list, filterDto: FilterDTO) -> list:
        if filterDto.id is None or filterDto.id == "":
            return self.data

        result = []
        filtration = FilterLogic(filterDto.type)
        for item in data:
            if filtration.type(filterDto.name, getattr(item, "unique_code")):
                result.append(item)

        return result

    def filter_name(self, data: list, filterDto: FilterDTO) -> list:
        if filterDto.name is None or filterDto.name == "":
            return self.data
        filter_data = []
        filtration = FilterLogic(filterDto.type)
        for item in data:
            if filtration.type(filterDto.name, getattr(item, "name")):
                filter_data.append(item)

        return filter_data

    def filter_period(self, data: list, start_period: datetime, end_period: datetime) -> list:
        if not isinstance(data, list):
            ArgumentTypeException('date_time', 'list')
        if not isinstance(start_period, datetime):
            ArgumentTypeException('start', 'datetime')
        if not isinstance(end_period, datetime):
            ArgumentTypeException('end', 'datetime')

        filter_data = []
        for item in data:
            if start_period <= getattr(item, "datetime") <= end_period:
                filter_data.append(item)

        return filter_data
