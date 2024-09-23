from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService
from src.utils.data_repository import DataRepository
import unittest


class TestDataRepository(unittest.TestCase):
    def test_data_keys(self):
        data_repository = DataRepository()
        settings_manager = SettingsManager()
        settings = settings_manager.settings
        service = StartService(data_repository, settings)
        service.create()

        assert data_repository.nomenclature_key() in data_repository.data
        assert data_repository.nomenclature_group_key() in data_repository.data
        assert data_repository.measurement_key() in data_repository.data
        assert data_repository.recipe_key() in data_repository.data

    def test_data_values(self):
        data_repository = DataRepository()
        settings_manager = SettingsManager()
        settings = settings_manager.settings
        service = StartService(data_repository, settings)
        service.create()

        assert len(data_repository.data[data_repository.nomenclature_key()]) > 0
        assert len(data_repository.data[data_repository.nomenclature_group_key()]) == 2
        assert len(data_repository.data[data_repository.measurement_key()]) == 3
        assert len(data_repository.data[data_repository.recipe_key()]) == 2