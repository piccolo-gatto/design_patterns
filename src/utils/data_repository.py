from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.event_type import EventType

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
    Ключ для хранения складов
    """

    @staticmethod
    def warehouse_key() -> str:
        return "warehouse"

    """
    Ключ для хранения транзакций
    """

    @staticmethod
    def transaction_key() -> str:
        return "transaction"


    """
    Перегрузка абстрактного метода
    """


    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)