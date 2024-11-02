from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService
from src.utils.data_repository import DataRepository
from src.models.transaction_type import TransactionType
from src.process.warehouse_turnover_process import WarehouseTurnoverProcess
import unittest


class TestWarehouse(unittest.TestCase):
    data_repository = DataRepository()
    settings_manager = SettingsManager()
    settings = settings_manager.settings
    service = StartService(data_repository, settings)
    service.create()

    def test_data_keys(self):
        assert self.data_repository.transaction_key() in self.data_repository.data

    def test_data_values(self):
        assert len(self.data_repository.data[self.data_repository.transaction_key()]) == 7

    def test_turnover_without_filter(self):
        transactions = self.data_repository.data[self.data_repository.transaction_key()]
        turnover = 0
        for transaction in transactions:
            if transaction.type == TransactionType.RECEIPT:
                turnover += transaction.count
            else:
                turnover -= transaction.count
        process = WarehouseTurnoverProcess()
        result = process.process(self.data_repository.data[self.data_repository.transaction_key()])

        assert len(result) > 0
        assert result[0].turnover == turnover