from src.utils.observe_service import ObserveService
from src.utils.event_type import EventType
from src.utils.data_repository import DataRepository
from src.abstract_models.abstract_logic import AbstractLogic
from src.utils.nomenclature_service import NomenclatureService


class RecipeService(AbstractLogic):
    def __init__(self, reposity: DataRepository):
        ObserveService.append(self)
        self.__reposity = reposity

    def update_recipes(self, request):
        recipes = self.__reposity.data(DataRepository.recipe_key(), [])
        for recipe in recipes:
            NomenclatureService.update_nomenclature_in_models(recipe, request)
        return {"status": "Рецепты успешно обновлены"}

    def handle_event(self, type: EventType, params):
        if type == EventType.CHANGE_NOMENCLATURE_FROM_RECIPE:
            return self.update_recipes(params)
        return {"status": "Ошибка обновления рецептов"}
