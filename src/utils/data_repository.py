from src.abstract_models.abstract_logic import AbstractLogic

"""
Репозиторий данных
"""


class DataRepository(AbstractLogic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataRepository, cls).__new__(cls)
        return cls.instance

    """
    Набор данных
    """

    @property
    def data(self):
        return self.__data

    """
    Ключ для хранения групп номенклатуры
    """

    @staticmethod
    def nomenclature_group_key() -> str:
        return "nomenclature_group"

    """
    Ключ для хранения номенклатуры
    """

    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature"


    """
    Ключ для хранения групп единиц измерения
    """

    @staticmethod
    def measurement_key() -> str:
        return "measurement"


    """
    Ключ для хранения рецептов
    """

    @staticmethod
    def recipe_key() -> str:
        return "recipe"


    """
    Перегрузка абстрактного метода
    """


    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)