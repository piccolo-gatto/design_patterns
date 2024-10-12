import unittest
from src.logics.domain_prototype import DomainPrototype
from src.dto.filter import FilterDTO
from src.utils.data_repository import DataRepository
from src.utils.settings_manager import SettingsManager
from src.utils.start_service import StartService

"""
Набор тестов для проверки прототипов
"""
class TestFilter(unittest.TestCase):
    manager = SettingsManager()
    repository = DataRepository()
    service = StartService(repository, manager)
    service.create()

    def test_filter_name_equals(self):
        data = self.repository.data[self.repository.nomenclature_key()]

        filter = FilterDTO()
        filter.name = "Пшеничная мука"
        filter.type = "equals"
        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, filter)

        assert len(filtered_data.data) == 1
        assert filtered_data.data[0].name == "Пшеничная мука"

    def test_filter_name_like(self):
        data = self.repository.data[self.repository.nomenclature_key()]

        filter = FilterDTO()
        filter.name = "С"
        filter.type = "like"
        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, filter)

        assert len(filtered_data.data) == 3
        assert "С" in filtered_data.data[0].name

    def test_filter_id_equals(self):
        data = self.repository.data[self.repository.nomenclature_key()]

        filter = FilterDTO()
        filter.id = data[0].unique_code
        filter.type = "equals"
        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, filter)
        print(len(filtered_data.data))
        assert len(filtered_data.data) > 1
        assert filtered_data.data[0].unique_code == data[0].unique_code

    def test_filter_id_like(self):
        data = self.repository.data[self.repository.nomenclature_key()]

        filter = FilterDTO()
        filter.id = "1"
        filter.type = "like"
        prototype = DomainPrototype(data)
        filtered_data = prototype.create(data, filter)

        assert len(filtered_data.data) > 1
        assert "1" in filtered_data.data[0].unique_code