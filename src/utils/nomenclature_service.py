from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType
from src.dto.filter import FilterDTO
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.data_repository import DataRepository
from src.dto.filter_type import FilterType
from src.logics.domain_prototype import DomainPrototype
from src.models.nomenclature_model import NomenclatureModel
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import EmptyException, UnknownValueException


class NomenclatureService(AbstractLogic):
    def __init__(self, repository: DataRepository):
        self.__repository = repository
        ObserveService.append(self)

    def get_nomenclature(self, request):
        unique_code = request.get("unique_code")
        if not unique_code:
            raise EmptyException()

        filter = FilterDTO()
        filter.id = unique_code
        filter.type = FilterType.EQUALS.value

        filter_data = self.filter_data(filter)
        return filter_data

    def add_nomenclature(self, request):
        unique_code = request.get("unique_code")
        if not unique_code:
            raise EmptyException()

        nomenclature = NomenclatureModel()
        self.data_to_nomenclature(nomenclature, request)
        self.__repository.data[DataRepository.nomenclature_key()].append(nomenclature)
        return nomenclature


    def update_nomenclature(self, request):
        unique_code = request.get("unique_code")
        if not unique_code:
            raise EmptyException()

        filter = FilterDTO()
        filter.id = unique_code
        filter.type = FilterType.EQUALS.value

        if not self.filter_data(filter)[0]:
            return EmptyException()
        self.data_to_nomenclature(self.filter_data(filter)[0], request)

        ObserveService.raise_event(EventType.CHANGE_NOMENCLATURE_FROM_RECIPE, request)
        ObserveService.raise_event(EventType.CHANGE_NOMENCLATURE_FROM_TRANSACTION, request)

        return self.filter_data(filter)[0]

    def delete_nomenclature(self, request):
        unique_code = request.get('unique_code')
        if not unique_code:
            raise EmptyException()

        filter = FilterDTO()
        filter.id = unique_code
        filter.type = FilterType.EQUALS.value
        nomenclature = next(iter(self.filter_data(filter)), None)

        if not nomenclature:
            raise EmptyException()

        if self.find_data(self, nomenclature, DataRepository.recipe_key()) or self.find_data(self, nomenclature, DataRepository.transaction_key()):
            raise Exception("Удаление запрещено! Данная номенклатура используется!")

        data = []
        for nomenclature in self.__repository.data[DataRepository.nomenclature_key()]:
            if nomenclature.unique_code != unique_code:
                data.append(nomenclature)

        self.__repository.data[DataRepository.nomenclature_key()] = data
        return data

    def filter_data(self, filter_model: FilterDTO, data_type=DataRepository.nomenclature_key()):
        data = self.__repository.data[data_type]
        prototype = DomainPrototype(data)
        result = prototype.create(data, filter_model)
        return result.data

    def data_to_nomenclature(self, model, request):
            if 'name' in request:
                model.name = request.get('name')

            if 'full_name' in request:
                model.full_name = request.get('full_name')

            if 'nomenclature_group' in request:
                group_filter = FilterDTO()
                group_filter.id = request.get('nomenclature_group_unique_code')
                group_filter.type = FilterType.EQUALS.value
                group = next(iter(self.filter_data(group_filter, DataRepository.nomenclature_group_key())), None)
                if not group:
                    raise UnknownValueException()
                model.group = group

            if 'measurement' in request:
                range_filter = FilterDTO()
                range_filter.id = request.get('measurement_unique_code')
                range_filter.type = FilterType.EQUALS.value
                range = next(iter(self.filter_data(range_filter, DataRepository.measurement_key())), None)
                if not range:
                    return UnknownValueException()
                model.range = range
    def update_nomenclature_in_models(self, model, request):
        unique_code = request.get('unique_code')
        if model in AbstractReference.__subclasses__() and model.unique_code == unique_code:
            self.data_to_nomenclature(model, request)
            return True

        elif isinstance(model, dict):
            for key, value in model.items():
                if self.update_nomenclature_in_models(value, unique_code, request):
                    return True

        elif isinstance(model, (list, tuple)):
            for item in model:
                if self.update_nomenclature_in_models(item, unique_code, request):
                    return True

        elif hasattr(model, '__dict__'):
            for attr_name in vars(model):
                attr_value = getattr(model, attr_name)
                if self.update_nomenclature_in_models(attr_value, unique_code, request):
                    return True
        return False

    def find_data(self, nomenclature: NomenclatureModel, data) -> bool:
            filter = FilterDTO()
            filter.unique_code=nomenclature.unique_code
            filter.type=FilterType.EQUALS.value
            return self.filter_data(filter, data) != 0

    def set_exception(self, ex: Exception):
        return super().set_exception(ex)

    def handle_event(self, type: EventType, params):
        return super().handle_event(type, params)
