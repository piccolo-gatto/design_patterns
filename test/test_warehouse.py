from src.utils.repository_manager import RepositoryManager
from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService
from src.utils.data_repository import DataRepository
from src.models.transaction_type import TransactionType
from src.process.warehouse_turnover_process import WarehouseTurnoverProcess
from src.process.warehouse_blocked_turnover_process import WarehouseBlockedTurnoverProcess
import unittest
from time import time


class TestWarehouse(unittest.TestCase):
    data_repository = DataRepository()
    settings_manager = SettingsManager()
    repository_manager = RepositoryManager(data_repository, settings_manager)
    service = StartService(data_repository, settings_manager, repository_manager)
    service.create()

    def test_data_keys(self):
        assert self.data_repository.transaction_key() in self.data_repository.data

    def test_data_values(self):
        assert len(self.data_repository.data[self.data_repository.transaction_key()]) == 1400

    def test_turnover_without_filter(self):
        transactions = self.data_repository.data[self.data_repository.transaction_key()]
        turnover = 0
        for transaction in transactions:
            if transaction.type == TransactionType.RECEIPT:
                turnover += transaction.count
            else:
                turnover -= transaction.count
        process = WarehouseTurnoverProcess()
        process.block_period = self.settings_manager.settings.block_period
        result = process.process(self.data_repository.data[self.data_repository.transaction_key()])

        assert len(result) > 0
        assert result[0].turnover == turnover


    def test_turnover_with_blocked_periods(self):
        transactions = self.data_repository.data[self.data_repository.transaction_key()]
        turnover = 0
        for transaction in transactions:
            if transaction.type == TransactionType.RECEIPT:
                turnover += transaction.count
            else:
                turnover -= transaction.count
        process = WarehouseTurnoverProcess()
        process.block_period = self.settings_manager.settings.block_period
        first_result = process.process(self.data_repository.data[self.data_repository.transaction_key()])

        process.block_period = "2024-10-01"
        second_result = process.process(self.data_repository.data[self.data_repository.transaction_key()])

        assert first_result == second_result

    def test_load_test_for_turnovers(self):
        block_dates = [
            "2024-01-01",
            "2024-10-01"
        ]
        result_times = []
        for block_date in block_dates:
            self.settings_manager.settings.block_period = block_date
            blocked_turnover_process = WarehouseBlockedTurnoverProcess()
            blocked_turnover_process.block_period = block_date

            start_time = time()
            blocked_turnover_process.process(self.data_repository.data[self.data_repository.transaction_key()])

            result_times.append(time() - start_time)

        with open('../data/load_test_for_turnovers.md', 'w', encoding="utf-8") as f:
            f.write("| Дата блокировки | Время (сек) |\n|-----------------|-------------|\n")
            for block_date, result_time in zip(block_dates, result_times):
                f.write(f"| {block_date} | {result_time:.10f} |\n")