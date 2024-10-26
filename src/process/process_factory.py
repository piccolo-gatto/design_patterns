from src.abstract_models.abstract_process import AbstractProcess
from src.utils.castom_exceptions import UnknownValueException


class ProcessFactory:
    __processes = {}

    def build_structure(self, process_class):
        self.__processes['warehouse_turnover'] = process_class

    def create(self, process_name: str) -> AbstractProcess:
        process = self.__processes.get(process_name)
        if not process:
            raise UnknownValueException()
        return process()
