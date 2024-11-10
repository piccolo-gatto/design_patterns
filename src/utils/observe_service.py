from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.castom_exceptions import ArgumentTypeException
from src.utils.event_type import EventType

class ObserveService:
    observers = []

    @staticmethod
    def append(service: AbstractLogic):

        if service is None:
            return

        if not isinstance(service, AbstractLogic):
            raise ArgumentTypeException("service", "AbstractLogic")

        items = list(map(lambda x: type(x).__name__, ObserveService.observers))
        found = type(service).__name__ in items
        if not found:
            ObserveService.observers.append(service)

    @staticmethod
    def raise_event(type: EventType, params):
        for instance in ObserveService.observers:
            if instance is not None:
                instance.handle_event(type, params)