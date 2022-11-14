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