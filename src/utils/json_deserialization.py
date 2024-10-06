import json
from src.abstract_models.abstract_logic import AbstractLogic
from src.abstract_models.abstract_reference import AbstractReference
from src.utils.castom_exceptions import ArgumentTypeException, EmptyException


class JSONDeserialization(AbstractLogic):
    __objects: list = []

    def __init__(self, model):
        self.model = model

    @property
    def objects(self) -> list:
        return self.__objects

    @objects.setter
    def objects(self, value: list):
        if not isinstance(value, list):
            raise ArgumentTypeException("objects", "list")

        self.__objects = value

    def open_report(self, file_path: str):
        if not isinstance(file_path, str):
            raise ArgumentTypeException("file_name", "str")
        with open(file_path, 'r') as f:
            data = json.load(f)
            if data is None:
                raise EmptyException()
        return data

    def get_objects(self, file_path: str):
        data = self.open_report(file_path)
        for item in data:
            obj = self.create(item, self.model)
            self.__objects.append(obj)

    def create(self, item, model: AbstractReference) -> AbstractReference:
        for key, value in item.items():
            deserialized = self.deserialize(model(), key, value)
            if hasattr(model(), key):
                setattr(model(), key, deserialized)

            return model()

    def deserialize(self, model, key, value):
        if isinstance(value, dict):
            model_atributes = model.__annotations__
            if not model_atributes:
                raise EmptyException()
            deserialized = self.create(value, model_atributes)
        elif isinstance(value, list):
            deserialized = []
            for val in value:
                deserialized.append(self.deserialize(model, key, val))
        else:
            deserialized = value
        return deserialized

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
