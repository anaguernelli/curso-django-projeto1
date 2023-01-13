from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val

# way 3


def strong_password(password):
    # ^ -> começar
    # $ -> terminar
    # {8,} -> password com pelo menos 8 chars
    # expressões regulares
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase, '
            'One lowercase letter and one number '
            'The length should be at least 8 characters'
            ),
            code='invalid'
        )
