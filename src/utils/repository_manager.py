import json
from src.abstract_models.abstract_logic import AbstractLogic
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.event_type import EventType
from src.utils.format_reporting import FormatReporting
from src.utils.data_repository import DataRepository
from src.utils.json_deserialization import JSONDeserialization
from src.utils.observe_service import ObserveService
from src.reports.report_factory import ReportFactory
from src.utils.settings_manager import SettingsManager



class RepositoryManager(AbstractLogic):
    __repository: DataRepository = None
    __settings_manager: SettingsManager = None
    __data_file: str = "data/repository.json"

    def __init__(self, repository: DataRepository, manager: SettingsManager) -> None:
        super().__init__()
        self.__repository = repository
        self.__settings_manager = manager
        ObserveService.append(self)

    def save_data(self):
        report = ReportFactory(self.__settings_manager).create(FormatReporting.JSON)
        try:
            reports = {}
            for key, value in self.__repository.data.items():
                if isinstance(value, list):
                    if not value:
                        reports[key] = []
                        continue
                    report.create(value)
                    reports[key] = json.loads(report.result)
            with open(self.__data_file, "w", encoding="utf-8") as file:
                json.dump(reports, file, ensure_ascii=False, indent=2)
        except Exception as e:
            raise e

    def load_data(self):
        data_methods = [method for method in dir(DataRepository)
                        if callable(getattr(DataRepository, method)) and method.endswith('_key')]
        data_map = {
            getattr(DataRepository, method)(): (method.replace('_key', ''), f"{method[0].upper()+method[1:].replace('_key', '')}Model")
            for method in data_methods
        }
        data_map[DataRepository.transaction_key()] = ("transaction", "WarehouseTransactionModel")
        try:
            with open(self.__data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

                for key, (data_key, model_name) in data_map.items():
                    for model in AbstractReference.__subclasses__():
                        if model.__name__ == model_name:
                            self.__repository.data[key] = JSONDeserialization(model).get_objects(data.get(data_key, []))
        except Exception as e:
            raise e

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)

        if type == EventType.SAVE_DATA:
            self.save_data()
        if type == EventType.LOAD_DATA:
            self.load_data()