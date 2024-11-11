import unittest
from main import app
from src.utils.nomenclature_service import NomenclatureService
from src.utils.event_type import EventType
from src.utils.data_repository import DataRepository
from src.models.nomenclature_model import NomenclatureModel
from src.utils.settings_manager import SettingsManager
from src.utils.recipe_manager import RecipeManager
from src.utils.start_service import StartService

class TestNomenclatureService(unittest.TestCase):
    app = app
    app.testing = True
    client = app.test_client()
    data_repository = DataRepository()
    settings_manager = SettingsManager()
    recipe_manager = RecipeManager()
    service = StartService(data_repository, settings_manager)

    def test_get_nomenclature(self):
        unique_code = self.data_repository.data[DataRepository.nomenclature_key()][0].unique_code
        response = self.client.get('/api/nomenclature/get', json={'unique_code': unique_code})
        data = response.json()

        assert response.status_code == 200

    def test_add_nomenclature(self):
        response = self.client.put('/api/nomenclature/add', json={
            'name': 'Фарш',
            'full_name': 'Фарш говяжий',
            'nonenclature_group_unique_code': self.data_repository.data[DataRepository.nomenclature_group_key()][0].unique_code,
            'measurement_id': self.data_repository.data[DataRepository.measurement_key()][0].unique_code
        })
        data = response.json()

        assert response.status_code == 200

    def test_update_nomenclature(self):
        unique_code = self.data_repository.data[DataRepository.nomenclature_key()][0].unique_code
        response = self.client.patch('/api/nomenclature/update', json={
            'unique_code': unique_code,
            'name': 'Огурец'
        })
        data = response.json()

        assert response.status_code == 200

    def test_delete_nomenclature(self):
        unique_code = self.data_repository.data[DataRepository.nomenclature_key()][0].unique_code
        response = self.client.delete('/api/nomenclature/delete', json={'unique_code': unique_code})
        data = response.json()

        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()