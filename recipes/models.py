# from email.policy import default
# from unittest.util import _MAX_LENGTH

from django.db import models

# Models converte o código em tabelas de db 

class Recipe(models.Model):
    title = models.CharField(max_length=65) 
    # CharField atua como varChar do bd
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    # para adicionar a data de 'lançamento', e não está sujeito a mudança
    updated_at = models.DateTimeField(auto_now=True)
    # para atualizar sempre que houver alterações
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')


# EDITED
# title description slug
# preparation_time preparation_time_unit
# servings servings_unit
# preparation_step
# preparation_step_is_html
# created_at updated_at
# is_published
# cover
# category (Relação)
# Author (Relação)
