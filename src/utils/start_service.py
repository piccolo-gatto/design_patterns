import random
import uuid
from datetime import datetime
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.data_repository import DataRepository
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.measurement_model import MeasurementModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.warehouse_model import WarehouseModel
from src.models.warehouse_transaction_model import WarehouseTransactionModel
from src.utils.recipe_manager import RecipeManager
from src.models.recipe_model import RecipeModel
from src.utils.settings_manager import SettingsManager
from src.models.settings_model import SettingsModel
from src.utils.event_type import EventType
from src.utils.repository_manager import RepositoryManager
from src.utils.observe_service import ObserveService

"""
Сервис для реализации первого старта приложения
"""


class StartService(AbstractLogic):
    __reposity: DataRepository = None
    __settings_manager: SettingsManager = None
    __repository_manager: RepositoryManager = None

    def __init__(self, reposity: DataRepository, manager: SettingsManager, repository_manager: RepositoryManager) -> None:
        super().__init__()
        self.__reposity = reposity
        self.__settings_manager = manager
        self.__repository_manager = repository_manager
        ObserveService.append(self)

    """
    Текущие настройки
    """

    @property
    def settings(self) -> SettingsModel:
        return self.__settings_manager.settings

    """
    Сформировать группы номенклатуры
    """

    def __create_nomenclature_groups(self):
        list = []
        list.append(NomenclatureGroupModel.default_group_cold())
        list.append(NomenclatureGroupModel.default_group_source())
        self.__reposity.data[DataRepository.nomenclature_group_key()] = list

    """
    Сформировать единицы измерения
    """

    def __create_measurements(self):
        list = []
        list.append(MeasurementModel.default_group_gram())
        list.append(MeasurementModel.default_group_milliliter())
        list.append(MeasurementModel.default_group_piece())
        self.__reposity.data[DataRepository.measurement_key()] = list

    """
    Сформировать рецепты
    """

    def __create_recipes(self):
        list = []
        manager = RecipeManager()
        manager.open()
        list.append(manager.recipe)
        manager.open("data/recipe2.md")
        list.append(manager.recipe)
        self.__reposity.data[DataRepository.recipe_key()] = list

    """
    Сформировать номенклатуру
    """

    def __create_nomenclature(self):
        list = []
        for recipe in self.__reposity.data[DataRepository.recipe_key()]:
            for ingredient in recipe.ingredients:
                if ingredient.nomenclature not in list:
                    list.append(ingredient.nomenclature)
        self.__reposity.data[DataRepository.nomenclature_key()] = list

    """
    Сформировать склады
    """

    def __create_warehouses(self):
        list = []
        list.append(WarehouseModel.default_warehouse_leninsky())
        list.append(WarehouseModel.default_warehouse_sverdlovsk())
        self.__reposity.data[DataRepository.warehouse_key()] = list

    """
    Сформировать транзакции
    """

    def __create_transactions(self):
        list = []
        for i in range(200):
            for nomenclature in self.__reposity.data[DataRepository.nomenclature_key()]:
                transaction = WarehouseTransactionModel()
                transaction.unique_code = uuid.uuid1().hex
                transaction.nomenclature = nomenclature
                transaction.measurement = nomenclature.measurement
                transaction.warehouse = random.choice([WarehouseModel.default_warehouse_leninsky(), WarehouseModel.default_warehouse_sverdlovsk()])
                transaction.count = random.randint(1, 1000)
                transaction.type = random.choice(['receipt', 'expenditure'])
                year = random.randint(1900, 2024)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                transaction.date = f"{year}-{month}-{day}"
                list.append(transaction)

        self.__reposity.data[DataRepository.transaction_key()] = list

    """
    Первый старт
    """

    def create(self):
        if self.__settings_manager.settings.first_start:
            self.__create_nomenclature_groups()
            self.__create_measurements()
            self.__create_recipes()
            self.__create_nomenclature()
            self.__create_warehouses()
            self.__create_transactions()
        else:
            self.__repository_manager.load_data()

    """
    Перегрузка абстрактного метода
    """

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)
