from src.dto.filter_type import FilterType
from src.utils.castom_exceptions import ArgumentTypeException


class FilterDTO:
    __name: str = ""
    __id: str = ""
    __type = FilterType.LIKE

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            ArgumentTypeException('name', str)
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            ArgumentTypeException('id', str)
        self.__id = value

    @property
    def type(self) -> FilterType:
        return self.__type

    @type.setter
    def type(self, value: FilterType):
        if not isinstance(value, FilterType):
            ArgumentTypeException('type', FilterType)
        self.__type = value

    def from_dict(self, data: dict):
        try:
            filter = FilterDTO()
            filter.name = data["name"]
            filter.id = data["unique_code"]
            filter.type = data["type"]

            return filter
        except Exception as e:
            raise e