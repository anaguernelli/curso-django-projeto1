from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from unittest.mock import patch

from .base import RecipeBaseFunctionalTest

from recipes.tests.test_recipe_base import RecipeMixin

import pytest


@pytest.mark.functional_test
# para executar o marker
# pytest -m 'functional_test' -rP
# para executar tudo menos 'functional_test'
# pytest -m 'not functional_test'
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest, RecipeMixin):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipe_not_found_messages(self):
        # live_server_url vai apenas pegar nossa url sem precisarmos digitá-la
        self.browser.get(self.live_server_url)
        # encontre elemento por tag name no body do html
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No Recipes Found Here !!', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I want'

        recipes[0].title = title_needed
        recipes[0].save()

        # usuário abre a página
        self.browser.get(self.live_server_url)

        # vê um campo de buscar com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita com título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # Usuário vê o que procurou na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, "recipe")),
            2
        )
