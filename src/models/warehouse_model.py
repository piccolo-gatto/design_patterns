import uuid
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException


class WarehouseModel(AbstractReference):
    __name: str = ""
    __address: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("name", "str")

        self.__name = value

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        if not isinstance(value, str):
            raise ArgumentTypeException("address", "str")

        self.__address = value

    @staticmethod
    def default_warehouse_sverdlovsk():
        item = WarehouseModel()
        item.unique_code = uuid.uuid1().hex
        item.name = "swerdlovsky"
        item.address = "ул. Майская, 3"
        return item

    @staticmethod
    def default_warehouse_leninsky():
        item = WarehouseModel()
        item.unique_code = uuid.uuid1().hex
        item.name = "leninsky"
        item.address = "ул. Промышленная, 21"
        return item


    def set_compare_mode(self, other_object) -> bool:
        return super().set_compare_mode(other_object)
