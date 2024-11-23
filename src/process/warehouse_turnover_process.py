from datetime import datetime
from src.abstract_models.abstract_process import AbstractProcess
from src.models.warehouse_turnover_model import WarehouseTurnoverModel
from src.models.transaction_type import TransactionType
from src.utils.castom_exceptions import ArgumentTypeException
from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType

class WarehouseTurnoverProcess(AbstractProcess):
    __blocked_data: dict = {}

    @property
    def blocked_data(self) -> dict:
        return self.__blocked_data

    @blocked_data.setter
    def blocked_data(self, value: dict):
        if not isinstance(value, dict):
            ObserveService.raise_event(EventType.ERROR_LOG, ArgumentTypeException("blocked_data", "dict"))
            raise ArgumentTypeException("blocked_data", "dict")

        self.__blocked_data = value

    def process(self, transactions: list):
        turnovers = {}
        for transaction in transactions:
            key = (transaction.warehouse.name, transaction.nomenclature.name, transaction.measurement.name)
            if transaction.date < self.block_period:
                if key not in turnovers:
                    turnovers[key] = WarehouseTurnoverModel()
                    turnovers[key].turnover = 0
                    turnovers[key].warehouse = transaction.warehouse
                    turnovers[key].nomenclature = transaction.nomenclature
                    turnovers[key].measurement = transaction.measurement
                    ObserveService.raise_event(EventType.INFO_LOG, "Создан новый сладской оборот")
                    ObserveService.raise_event(EventType.DEBUG_LOG, turnovers[key])
                if transaction.type == TransactionType.RECEIPT.value:
                    turnovers[key].turnover += transaction.count
                else:
                    turnovers[key].turnover -= transaction.count

        for key, turnover in self.blocked_data.items():
            if key in turnovers:
                turnovers[key].turnover += turnover.turnover
            else:
                turnovers[key] = turnover

        return list(turnovers.values())