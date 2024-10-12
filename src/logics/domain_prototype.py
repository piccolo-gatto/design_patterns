from src.abstract_models.abstract_prototype import AbstractPrototype
from src.dto.filter import FilterDTO
from src.dto.filter_logic import FilterLogic


class DomainPrototype(AbstractPrototype):

    def __init__(self, source: list) -> None:
        super().__init__(source)

    def create(self, data: list, filterDto: FilterDTO):
        super().create(data, filterDto)
        self.data = self.filter_name(data, filterDto)
        self.data = self.filter_id(self.data, filterDto)
        return DomainPrototype(self.data)

    def filter_id(self, data: list, filterDto: FilterDTO) -> list:
        if filterDto.id is None or filterDto.id == "":
            return self.data

        result = []
        filtration = FilterLogic(filterDto.type)
        for item in data:
            print(filterDto.name, getattr(item, "unique_code"))
            if filtration.type(filterDto.name, getattr(item, "unique_code")):
                result.append(item)

        return result

    def filter_name(self, data: list, filterDto: FilterDTO) -> list:
        if filterDto.name is None or filterDto.name == "":
            return self.data
        filter_data = []
        filtration = FilterLogic(filterDto.type)
        for item in data:
            if filtration.type(filterDto.name, getattr(item, "name")):
                filter_data.append(item)

        return filter_data
