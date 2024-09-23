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

        assert nomenclature.name == "nomen1"
        assert nomenclature.full_name == "Nomenclature 1"
        assert nomenclature.group == nomenclature_group

    def test_new_nomenclature_group(self):
        nomenclature_group = NomenclatureGroupModel()
        nomenclature_group.name = "nomen_group1"

        assert nomenclature_group.name == "nomen_group1"

    def test_new_warehouse(self):
        warehouse = WarehouseModel()
        warehouse.name = "warehouse1"

        assert warehouse.name == "warehouse1"

    def test_new_organization(self):
        organization = OrganizationModel()
        organization.inn = "380930934984"
        organization.bic = "044525225"
        organization.account = "11111111111"
        organization.organization_type = "12345"

        assert organization.inn == "380930934984"
        assert organization.bic == "044525225"
        assert organization.account == "11111111111"
        assert organization.organization_type == "12345"

    def test_organization_from_settings(self):
        manager = SettingsManager()
        organization = OrganizationModel()
        organization.load_settings(manager)

        assert organization.inn == "380080920202"
        assert organization.bic == "044525225"
        assert organization.account == "12345678900"
        assert organization.organization_type == "11111"

    def test_new_measurement(self):
        measurement = MeasurementModel()
        measurement.name = "measurement"
        measurement.coefficient = 1

        assert measurement.name == "measurement"
        assert measurement.coefficient == 1
        assert measurement.base == None

    def test_base_measurement(self):
        measurement = MeasurementModel()
        base_measurement = MeasurementModel()
        measurement.name = "measurement"
        measurement.coefficient = 1000
        base_measurement.name = "base_measurement"
        base_measurement.coefficient = 1
        measurement.base = base_measurement

        assert measurement.name == "measurement"
        assert measurement.coefficient == 1000
        assert measurement.base.name == "base_measurement"
        assert measurement.base.coefficient == 1


if __name__ == '__main__':
    unittest.main()
