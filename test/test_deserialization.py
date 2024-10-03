import unittest
import os
from src.utils.start_service import StartService
from src.utils.data_repository import DataRepository
from src.utils.json_deserialization import JSONDeserialization
from src.models.measurement_model import MeasurementModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils.settings_manager import SettingsManager


class TestReporting(unittest.TestCase):
    def test_nomenclature_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        report = JSONDeserialization(NomenclatureModel)
        report.open_report('reports/nomenclature_report.json')
        data = repository.data[repository.nomenclature_key()]

        assert len(report.objects) == len(data)
        for i in range(len(data)):
            assert report.objects[i] == data[i]

    def test_nomenclature_group_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        report = JSONDeserialization(NomenclatureGroupModel)
        report.open_report('reports/nomenclature_group_report.json')
        data = repository.data[repository.nomenclature_group_key()]

        assert len(report.objects) == len(data)
        for i in range(len(data)):
            assert report.objects[i] == data[i]

    def test_measurement_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        report = JSONDeserialization(MeasurementModel)
        report.open_report('reports/measurement_report.json')
        data = repository.data[repository.measurement_key()]

        assert len(report.objects) == len(data)
        for i in range(len(data)):
            assert report.objects[i] == data[i]

    def test_recipe_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        report = JSONDeserialization(RecipeModel)
        report.open_report('reports/recipe_report.json')
        data = repository.data[repository.recipe_key()]

        assert len(report.objects) == len(data)
        for i in range(len(data)):
            assert report.objects[i] == data[i]
