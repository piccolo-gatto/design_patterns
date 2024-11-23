from src.abstract_models.abstract_process import AbstractProcess
from src.utils.castom_exceptions import UnknownValueException
from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType


class ProcessFactory:
    __processes = {}

    def build_structure(self, process_class):
        self.__processes['warehouse_turnover'] = process_class

    def create(self, process_name: str) -> AbstractProcess:
        process = self.__processes.get(process_name)
        if not process:
            ObserveService.raise_event(EventType.ERROR_LOG, "Указанный процесс не найден")
            raise UnknownValueException()
        return process()
