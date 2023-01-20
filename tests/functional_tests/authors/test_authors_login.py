import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorBaseTest


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

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )

    def test_form_login_is_invalid(self):
        # User abre a página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User vê o form de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # E tenta enviar valores vazios
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        # User envia valores "vazios"
        username.send_keys(' ')
        password.send_keys(' ')

        form.submit()

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    # is_authenticated
    def test_form_login_invalid_credentials(self):
        # User abre página de login
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        # User vê form de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # E tenta enviar valores com dados que nao correspondem
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        # Envia form
        form.submit()

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
