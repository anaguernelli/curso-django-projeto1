from .base import AuthorBaseTest


class AuthorsRegisterTest(AuthorBaseTest):
    def test_test(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        self.sleep(5)
