from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.data_repository import DataRepository
# from src.Core.validator import validator
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.measurement_model import MeasurementModel
from src.models.nomenclature_model import NomenclatureModel
from src.utils.recipe_manager import RecipeManager
from src.models.recipe_model import RecipeModel
from src.utils.settings_manager import SettingsManager
from src.models.settings_model import SettingsModel

"""
Сервис для реализации первого старта приложения
"""


class StartService(AbstractLogic):
    __reposity: DataRepository = None
    __settings_manager: SettingsManager = None

    def __init__(self, reposity: DataRepository, manager: SettingsManager) -> None:
        super().__init__()
        # validator.validate(reposity, data_reposity)
        # validator.validate(manager, settings_manager)
        self.__reposity = reposity
        self.__settings_manager = manager

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
        manager.open("../data/recipe2.md")
        list.append(manager.recipe)
        self.__reposity.data[DataRepository.recipe_key()] = list

    """
    Сформировать номенклатуру
    """

    def __create_nomenclature(self):
        list = []
        for recipe in self.__reposity.data[DataRepository.recipe_key()]:
            for ingredient in recipe.ingredients:
                if ingredient['nomenclature'] not in list:
                    list.append(ingredient['nomenclature'])
        self.__reposity.data[DataRepository.nomenclature_key()] = list

    """
    Первый старт
    """

    def create(self):
        self.__create_nomenclature_groups()
        self.__create_measurements()
        self.__create_recipes()
        self.__create_nomenclature()

    """
    Перегрузка абстрактного метода
    """

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
