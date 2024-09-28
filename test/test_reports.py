import unittest
import os
from src.utils.start_service import StartService
from src.utils.data_repository import DataRepository
from src.reports.report_factory import ReportFactory
from src.reports.csv_report import CSVReport
from src.reports.markdown_report import MDReport
from src.reports.json_report import JSONReport
from src.reports.xml_report import XMLReport
from src.reports.rtf_report import RTFReport
from src.utils.settings_manager import SettingsManager


class TestReporting(unittest.TestCase):

    def test_report_formats(self):
        manager = SettingsManager()
        factory = ReportFactory(manager)

        factory.get_formats()
        assert len(factory.reports_setting) != 0


    def test_csv_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        reports = {}

        measurement_report = CSVReport()
        measurement_report.create(repository.data[repository.measurement_key()])
        reports["measurement_report"] = measurement_report

        nomenclature_report = CSVReport()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        nomenclature_group_report = CSVReport()
        nomenclature_group_report.create(repository.data[repository.nomenclature_group_key()])
        reports["nomenclature_group_report"] = nomenclature_group_report

        recipe_report = CSVReport()
        recipe_report.create(repository.data[repository.recipe_key()])
        reports["recipe_report"] = recipe_report

        assert measurement_report.result != ""
        assert nomenclature_report.result != ""
        assert nomenclature_group_report.result != ""
        assert recipe_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.csv', 'w', encoding='utf-8') as f:
                f.write(value.result)

    def test_md_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        reports = {}

        measurement_report = MDReport()
        measurement_report.create(repository.data[repository.measurement_key()])
        reports["measurement_report"] = measurement_report

        nomenclature_report = MDReport()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        nomenclature_group_report = MDReport()
        nomenclature_group_report.create(repository.data[repository.nomenclature_group_key()])
        reports["nomenclature_group_report"] = nomenclature_group_report

        recipe_report = MDReport()
        recipe_report.create(repository.data[repository.recipe_key()])
        reports["recipe_report"] = recipe_report

        assert measurement_report.result != ""
        assert nomenclature_report.result != ""
        assert nomenclature_group_report.result != ""
        assert recipe_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.md', 'w', encoding='utf-8') as f:
                f.write(value.result)


    def test_json_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        reports = {}

        measurement_report = JSONReport()
        measurement_report.create(repository.data[repository.measurement_key()])
        reports["measurement_report"] = measurement_report

        nomenclature_report = JSONReport()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        nomenclature_group_report = JSONReport()
        nomenclature_group_report.create(repository.data[repository.nomenclature_group_key()])
        reports["nomenclature_group_report"] = nomenclature_group_report

        recipe_report = JSONReport()
        recipe_report.create(repository.data[repository.recipe_key()])
        reports["recipe_report"] = recipe_report

        assert measurement_report.result != ""
        assert nomenclature_report.result != ""
        assert nomenclature_group_report.result != ""
        assert recipe_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.json', 'w', encoding='utf-8') as f:
                f.write(value.result)

    def test_xml_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        reports = {}

        measurement_report = XMLReport()
        measurement_report.create(repository.data[repository.measurement_key()])
        reports["measurement_report"] = measurement_report

        nomenclature_report = XMLReport()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        nomenclature_group_report = XMLReport()
        nomenclature_group_report.create(repository.data[repository.nomenclature_group_key()])
        reports["nomenclature_group_report"] = nomenclature_group_report

        recipe_report = XMLReport()
        recipe_report.create(repository.data[repository.recipe_key()])
        reports["recipe_report"] = recipe_report

        assert measurement_report.result != ""
        assert nomenclature_report.result != ""
        assert nomenclature_group_report.result != ""
        assert recipe_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.xml', 'w', encoding='utf-8') as f:
                f.write(value.result)


    def test_rtf_reports(self):
        manager = SettingsManager()
        repository = DataRepository()
        service = StartService(repository, manager)
        service.create()
        reports = {}

        measurement_report = RTFReport()
        measurement_report.create(repository.data[repository.measurement_key()])
        reports["measurement_report"] = measurement_report

        nomenclature_report = RTFReport()
        nomenclature_report.create(repository.data[repository.nomenclature_key()])
        reports["nomenclature_report"] = nomenclature_report

        nomenclature_group_report = RTFReport()
        nomenclature_group_report.create(repository.data[repository.nomenclature_group_key()])
        reports["nomenclature_group_report"] = nomenclature_group_report

        recipe_report = RTFReport()
        recipe_report.create(repository.data[repository.recipe_key()])
        reports["recipe_report"] = recipe_report

        assert measurement_report.result != ""
        assert nomenclature_report.result != ""
        assert nomenclature_group_report.result != ""
        assert recipe_report.result != ""

        if not os.path.exists("reports"):
            os.makedirs("reports")
        for key, value in reports.items():
            with open(f'reports/{key}.rtf', 'w', encoding='utf-8') as f:
                f.write(value.result)