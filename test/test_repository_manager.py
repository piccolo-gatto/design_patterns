import json
import unittest
import os

from src.dto.transaction_filter import TransactionFilterDTO
from src.logics.transaction_prototype import TransactionPrototype
from src.process.warehouse_turnover_process import WarehouseTurnoverProcess
from src.reports.tbs_report import TBSReport
from src.utils.data_repository import DataRepository
from src.utils.settings_manager import SettingsManager
from src.utils.repository_manager import RepositoryManager
from src.utils.start_service import StartService


class TestRepositoryManager(unittest.TestCase):
    repository = DataRepository()
    settings_manager = SettingsManager()
    repository_manager = RepositoryManager(repository, settings_manager)
    service = StartService(repository, settings_manager, repository_manager)
    service.create()

    def test_save_data(self):
        file_path = "../data/repository.json"
        assert os.path.exists(file_path) == False
        self.repository_manager.save_data()
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            data = json.loads(content)
        os.remove(file_path)
        assert len(data) != 0
        assert data.get("nomenclature", [])[0]['name'] == self.repository.data[self.repository.nomenclature_key()][0].name

    def test_load_data(self):
        before_value = self.repository.data[self.repository.nomenclature_key()][0]
        self.repository_manager.save_data()
        self.repository_manager.load_data()
        os.remove("../data/repository.json")
        new_value = self.repository.data[self.repository.nomenclature_key()][0]

        assert before_value == new_value

    def test_tbs_report(self):
        filter_before = {
            "warehouse": {
                "name": 'leninsky',
                "unique_code": "",
                "type": "equals"},
            "nomenclature": {
                "name": "",
                "unique_code": "",
                "type": "equals"},
            "start_period": "1900-01-01",
            "end_period": "2024-11-01"
        }
        filter = TransactionFilterDTO().from_dict(filter_before)
        f_data = self.repository.data['transaction']

        prototype = TransactionPrototype(f_data)
        filtered_data = prototype.create(f_data, filter)
        process = WarehouseTurnoverProcess()
        process.block_period = self.settings_manager.settings.block_period
        result_before = process.process(filtered_data.data)
        filter_between = {
            "warehouse": {
                "name": 'leninsky',
                "unique_code": "",
                "type": "equals"},
            "nomenclature": {
                "name": "",
                "unique_code": "",
                "type": "equals"},
            "start_period": "2024-11-01",
            "end_period": "2024-11-16"
        }
        filter = TransactionFilterDTO().from_dict(filter_between)
        filtered_data = prototype.create(f_data, filter)
        result_between = process.process(filtered_data.data)
        turnover_data = [result_before, result_between]

        report = TBSReport()
        report.create(turnover_data)
        assert len(report.result) != 0
        result = json.loads(report.result)
        assert result[0]['warehouse'] == 'leninsky'