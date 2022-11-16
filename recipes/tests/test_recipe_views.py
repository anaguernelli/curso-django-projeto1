from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views

# O 'resolve' resolve qual função está sendo usada

class RecipeViewsTest(TestCase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        # pôr só '/' na url é hard coded, desta forma acima 
        # está trabalhando de forma dinâmica
        self.assertIs(view.func, views.home)
        # está comparando se a função view É a view de home

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
    
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found</h1>', 
            response.content.decode('utf-8'))
# o content é o conteúdo HTML de recipes:home e está sendo imposto como string
# enquanto q o assertIn() procura pro 'recipes not found' dentro deste content