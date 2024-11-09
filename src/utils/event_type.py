from enum import Enum

"""
Типы событий
"""
class EventType(Enum):
    DELETE_NOMENCLATURE = 1
    CHANGE_NOMENCLATURE = 2
    CHANGE_RANGE = 3
    CHANGE_NOMENCLATURE_FROM_RECIPE = 4
    CHANGE_NOMENCLATURE_FROM_TRANSACTION = 5