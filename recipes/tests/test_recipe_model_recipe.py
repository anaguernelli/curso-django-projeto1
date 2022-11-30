from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_the_test(self):
        self.recipe.title = 'a' * 66

        # ele vai retornar OK após executar o full_clean e retornar um erro
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
