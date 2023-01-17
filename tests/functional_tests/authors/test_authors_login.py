import pytest
from .base import AuthorBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='user_name',
            password=string_password,
        )

        # User abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User vê o form de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User envia o formulário
        form.submit()

        # User vê a mensagem de login com sucesso e seu nome
        self.assertIn(
            f'You are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
