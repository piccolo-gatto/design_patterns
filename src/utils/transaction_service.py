from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType
from src.utils.data_repository import DataRepository
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.nomenclature_service import NomenclatureService


class TransactionService(AbstractLogic):
    def __init__(self, reposity: DataRepository):
        ObserveService.append(self)
        self.__reposity = reposity

    def update_transactions(self, request):
        transactions = self.__reposity.data(DataRepository.transaction_key(), [])
        for transaction in transactions:
            NomenclatureService.update_nomenclature_in_models(transaction, request)
        return {"status": "Транзакции успешно обновлены"}

    def handle_event(self, type: EventType, params):
        if type == EventType.CHANGE_NOMENCLATURE_FROM_TRANSACTION:
            return self.update_transactions(params)
        return {"status": "Ошибка обновления транзакций"}
