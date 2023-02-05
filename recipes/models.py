from collections import defaultdict
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Value, F
from django.db.models.functions import Concat
from tag.models import Tag
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
                )
            )[:5]


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    # CharField atua como varChar do bd
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
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
    cover = models.ImageField(
      upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    # vai criar uma lista das tags
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    # Atalho para reverse
    def get_absolute_url(self):
        return reverse("recipes:recipe", args={self.id, })

    @staticmethod
    def resize_image(image, new_width=800):
        # uma junção entre o media_root e nome da img
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        # pegando a imagem do pillow
        image_pillow = Image.open(image_full_path)
        # size "desempacota" do 1 e 2 o atributo da tupla da variável
        original_width, original_height = image_pillow.size

        # se for menor q o max de largura, não executará nada
        if original_width <= new_width:
            image_pillow.close()
            return

        # se for maior que 800px, reduziremos essa img
        new_height = round((new_width * original_height) / original_width)

        # LANCZOS utilizado pra fazer resize da img
        # (diminui a img mantendo as proporções)
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=60,
        )

    # Criar slug
    def save(self, *args, **kwargs):
        # pre-save
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        # nao esqueça de retornar oq está sobrescrevendo
        return saved
        # post-save

    def clean(self, *args, **kwargs):
        # dicionário em que agr toda chave é uma lista
        error_messages = defaultdict(list)

        # podemos pegar a Recipe dentro dela mesma
        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
