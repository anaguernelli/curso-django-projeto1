from django.core.exceptions import ValidationError
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from authors.validators import AuthorRecipeValidator


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria um dicionário e qualquer chave q criar dentro dele
        # Vai ter como padrão uma lista vazia inicialmente
        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                },
            ),

            # Torna o field um conjunto de opções p User selecionar
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Pieces', 'Pieces'),
                    ('People', 'People'),
                ),
            ),

            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
