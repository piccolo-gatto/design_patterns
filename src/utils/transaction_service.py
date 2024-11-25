from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType
from src.utils.data_repository import DataRepository
from src.abstract_models.abstract_logic import AbstractLogic


class TransactionService(AbstractLogic):
    def __init__(self, repository: DataRepository):
        ObserveService.append(self)
        self.__repository = repository

    def update_transactions(self, data):
        transactions = self.__repository.data(DataRepository.transaction_key(), [])
        for transaction in transactions:
            data.update_nomenclature_in_models(transaction)
            ObserveService.raise_event(EventType.INFO_LOG, "Номенклатура внутри транзакции обновлена")
            ObserveService.raise_event(EventType.DEBUG_LOG, transaction)
        return {"status": "Транзакции успешно обновлены"}

    def handle_event(self, type: EventType, params):
        if type == EventType.CHANGE_NOMENCLATURE_FROM_TRANSACTION:
            return self.update_transactions(params)
        return {"status": "Ошибка обновления транзакций"}
