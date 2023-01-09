from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


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
        ('email', 'The e-mail must be valid'),
        ('username',
            'Obrigatório. 150 caracteres ou menos. Letras, '
            'números e @/./+/-/_ apenas.'),
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
