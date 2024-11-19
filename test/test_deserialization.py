import unittest
from src.utils.start_service import StartService
from src.utils.data_repository import DataRepository
from src.utils.json_deserialization import JSONDeserialization
from src.models.measurement_model import MeasurementModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils.settings_manager import SettingsManager
from src.utils.castom_exceptions import EmptyException
from src.utils.repository_manager import RepositoryManager


"""
Тестовая пустая модель
"""
class EmptyModel():
    pass


"""
Тесты для проверки десериализации json
"""
class TestReporting(unittest.TestCase):
    manager = SettingsManager()
    repository = DataRepository()
    repository_manager = RepositoryManager(repository, manager)
    service = StartService(repository, manager, repository_manager)
    service.create()


    """
    Тест выгрузки данных из json в NomenclatureModel
    """
    def test_nomenclature_reports(self):
        report = JSONDeserialization(NomenclatureModel)
        report.open_report('reports/nomenclature_report.json')
        data = self.repository.data[self.repository.nomenclature_key()]

        assert len(report.objects) == len(data)

        for i in range(len(data)):
            assert report.objects[i] == data[i]


    """
    Тест выгрузки данных из json в NomenclatureGroupModel
    """
    def test_nomenclature_group_reports(self):
        report = JSONDeserialization(NomenclatureGroupModel)
        report.open_report('reports/nomenclature_group_report.json')
        data = self.repository.data[self.repository.nomenclature_group_key()]

        assert len(report.objects) == len(data)

        for i in range(len(data)):
            assert report.objects[i] == data[i]


    """
    Тест выгрузки данных из json в MeasurementModel
    """
    def test_measurement_reports(self):
        report = JSONDeserialization(MeasurementModel)
        report.open_report('reports/measurement_report.json')
        data = self.repository.data[self.repository.measurement_key()]

        assert len(report.objects) == len(data)

        for i in range(len(data)):
            assert report.objects[i] == data[i]


    """
    Тест выгрузки данных из json в RecipeModel
    """
    def test_recipe_reports(self):
        report = JSONDeserialization(RecipeModel)
        report.open_report('reports/recipe_report.json')
        data = self.repository.data[self.repository.recipe_key()]

        assert len(report.objects) == len(data)

        for i in range(len(data)):
            assert report.objects[i] == data[i]


    """
    Тест на десериализацию в пустую модель
    """
    def test_empty_model(self):
        report = JSONDeserialization(EmptyModel)

        with self.assertRaises(EmptyException):
            report.deserialize(EmptyModel, 'test_key', {'test_dict_key': 'test_dict_value'})
