from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
