from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


# testes unitários
class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: Will'),
        ('last_name', 'Ex.: Smith'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('password',
            'Password must have at least one uppercase, '
            'One lowercase letter and one number '
            'The length should be at least 8 characters'),
        ('email', 'The e-mail must be valid.'),
        ('username',
            'Username must have letters, numbers '
            'or one of those @/./+/-/_.'
            'The length should be between 4 and 150 characters'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label

        self.assertEqual(current, needed)


# testes d e integração
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anymail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1'}
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )
        # conteúdo renderizado da tela
        self.assertIn(msg, response.content.decode('utf-8'))
        # form do contexto
        self.assertIn(msg, response.context['form'].errors.get(field))

    # testando o erro
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'ana'
        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )

        msg = 'Username must have at least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )

        msg = 'Username must have less than 150 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )

        msg = (
            'Password must have at least one uppercase, '
            'One lowercase letter and one number '
            'The length should be at least 8 characters'
        )

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@A123abc123'
        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1234'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True)

        msg = 'Password and password2 must be equal'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_register_create_view_returns_404(self):
        response = self.client.get(reverse('authors:register_create'))

        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )
        response = self.client.post(
            reverse('authors:register_create'),
            data=self.form_data,
            follow=True
        )
        msg = 'User e-mail is already in use'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_Login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'Anao',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='Anao',
            password='@Bc123456'
        )

        self.assertTrue(is_authenticated)