import unittest
from src.utils.settings_manager import SettingsManager
from src.models.organization_model import OrganizationModel
from src.models.measurement_model import MeasurementModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.warehouse_model import WarehouseModel


class TestModels(unittest.TestCase):

    def test_new_nomenclature(self):
        nomenclature = NomenclatureModel()
        nomenclature_group = NomenclatureGroupModel()
        nomenclature.name = "nomen1"
        nomenclature.full_name = "Nomenclature 1"
        nomenclature.group = nomenclature_group

        self.assertEqual(nomenclature.name, "nomen1")
        self.assertEqual(nomenclature.full_name, "Nomenclature 1")
        self.assertEqual(nomenclature.group, nomenclature_group)

    def test_new_nomenclature_group(self):
        nomenclature_group = NomenclatureGroupModel()
        nomenclature_group.name = "nomen_group1"

        self.assertEqual(nomenclature_group.name, "nomen_group1")

    def test_new_warehouse(self):
        warehouse = WarehouseModel()
        warehouse.name = "warehouse1"

        self.assertEqual(warehouse.name, "warehouse1")

    def test_new_organization(self):
        organization = OrganizationModel()
        organization.inn = "380930934984"
        organization.bic = "044525225"
        organization.account = "11111111111"
        organization.organization_type = "12345"

        self.assertEqual(organization.inn, "380930934984")
        self.assertEqual(organization.bic, "044525225")
        self.assertEqual(organization.account, "11111111111")
        self.assertEqual(organization.organization_type, "12345")

    def test_organization_from_settings(self):
        manager = SettingsManager()
        organization = OrganizationModel()
        organization.load_settings(manager)

        self.assertEqual(organization.inn, "380080920202")
        self.assertEqual(organization.bic, "044525225")
        self.assertEqual(organization.account, "12345678900")
        self.assertEqual(organization.organization_type, "11111")

    def test_new_measurement(self):
        measurement = MeasurementModel()
        measurement.name = "measurement"
        measurement.coefficient = 1

        self.assertEqual(measurement.name, "measurement")
        self.assertEqual(measurement.coefficient, 1)
        self.assertEqual(measurement.base, None)

    def test_base_measurement(self):
        measurement = MeasurementModel()
        base_measurement = MeasurementModel()
        measurement.name = "measurement"
        measurement.coefficient = 1000
        base_measurement.name = "base_measurement"
        base_measurement.coefficient = 1
        measurement.base = base_measurement

        self.assertEqual(measurement.name, "measurement")
        self.assertEqual(measurement.coefficient, 1000)
        self.assertEqual(measurement.base.name, "base_measurement")
        self.assertEqual(measurement.base.coefficient, 1)


if __name__ == '__main__':
    unittest.main()
