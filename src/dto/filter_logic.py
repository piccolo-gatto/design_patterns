from datetime import datetime
from src.dto.filter_type import FilterType
from src.utils.castom_exceptions import ArgumentTypeException


class FilterLogic():
    def __init__(self, filter_type: FilterType):
        if not isinstance(filter_type, FilterType):
            ArgumentTypeException('filter_type', 'FilterType')
        self.type = getattr(self, filter_type)

    def equals(self, first: str, second: str) -> bool:
        if not isinstance(first, str):
            ArgumentTypeException('first', 'str')
        if not isinstance(second, str):
            ArgumentTypeException('second', 'str')

        return first == second

    def like(self, substring: str, string: str) -> bool:
        if not isinstance(string, str):
            ArgumentTypeException('str', 'str')
        if not isinstance(substring, str):
            ArgumentTypeException('substr', 'str')

        return substring in string

