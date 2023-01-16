# vai pegar o static, pois precisamos do css junto
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
import time


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, sec=5):
        time.sleep(sec)


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipe_not_found_messages(self):
        # live_server_url vai apenas pegar nossa url sem precisarmo digitá-la
        self.browser.get(self.live_server_url)
        # encontre elemento por tag name no body do html
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No Recipes Found Here !!', body.text)
