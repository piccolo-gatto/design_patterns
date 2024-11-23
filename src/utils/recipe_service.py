from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType
from src.utils.data_repository import DataRepository
from src.abstract_models.abstract_logic import AbstractLogic


class RecipeService(AbstractLogic):
    def __init__(self, repository: DataRepository):
        ObserveService.append(self)
        self.__repository = repository

    def update_recipes(self, data):
        recipes = self.__repository.data(DataRepository.recipe_key(), [])
        for recipe in recipes:
            data.update_nomenclature_in_models(recipe)
            ObserveService.raise_event(EventType.INFO_LOG, "Номенклатура внутри рецепта обновлена")
            ObserveService.raise_event(EventType.DEBUG_LOG, recipe)
        return {"status": "Рецепты успешно обновлены"}

    def handle_event(self, type: EventType, params):
        if type == EventType.CHANGE_NOMENCLATURE_FROM_RECIPE:
            return self.update_recipes(params)
        return {"status": "Ошибка обновления рецептов"}
