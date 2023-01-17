from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
import time

class AuthorBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qty=10):
        time.sleep(qty)
