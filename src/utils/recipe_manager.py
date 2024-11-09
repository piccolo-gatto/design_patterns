import re
from src.models.recipe_model import RecipeModel
from src.abstract_models.abstract_logic import AbstractLogic
from src.models.nomenclature_model import NomenclatureModel
from src.models.measurement_model import MeasurementModel
from src.models.ingredient_model import IngredientModel
from src.models.process_model import ProcessModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils.event_type import EventType

class RecipeManager(AbstractLogic):
    __file_name: str = "../data/recipe1.md"
    __recipe: RecipeModel = None

    """
    Открыть и загрузить рецепт
    """

    def open(self, file_name: str = ""):
        if file_name != "":
            self.__file_name = file_name
        self.__recipe = RecipeModel()
        self.__recipe.ingredients = []
        self.__recipe.process = []
        with open(self.__file_name, 'r') as f:
            lines = f.read()
            self.__recipe.name = re.search(r'#{1,1} (.+)', lines).group(1).strip()
            self.__recipe.count = int(re.search(r'#{4,4} `(.+) ', lines).group(1).strip())
            self.__recipe.minutes = int(re.search(r'Время приготовления: `(.+) ', lines).group(1).strip())
            ingredients_data = re.search(r'\| Ингредиенты\s+\|\s+Граммовка \|\n\|\W+\|\W+(\|.+)\n##', lines,
                                         re.DOTALL).group(1).strip()

            for row in ingredients_data.split('\n'):
                cols = row.split('|')
                nomen = NomenclatureModel()
                ingredient = IngredientModel()
                nomen.name = ingredient.name = cols[1].strip()
                measurement = MeasurementModel()
                count, measurement.name = cols[2].strip().split(" ")
                nomen.measurement = measurement
                nomen.group = NomenclatureGroupModel.default_group_source()
                ingredient.count = int(count)
                ingredient.nomenclature = nomen
                ingredient.measurement = measurement
                self.__recipe.ingredients.append(ingredient)
            process_data = re.search(r'## ПОШАГОВОЕ ПРИГОТОВЛЕНИЕ\nВремя приготовления: `\d+ мин`\n(.+)', lines,
                                     re.DOTALL).group(1).strip()
            for row in re.split(r'\d+\. ', process_data):
                if row != "":
                    process = ProcessModel()
                    process.name = f"{len(self.__recipe.process) + 1}"
                    process.content = row.strip()
                    self.__recipe.process.append(process)

    """
    Загруженный рецепт
    """

    @property
    def recipe(self) -> RecipeModel:
        return self.__recipe

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: EventType, params):
        super().handle_event(type, params)