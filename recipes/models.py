from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag


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
    title = models.CharField(max_length=65)
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
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    # Atalho para reverse
    def get_absolute_url(self):
        return reverse("recipes:recipe", args={self.id, })

    # Criar slug
    def save(self, *args, **kwargs):
        # Toda vez q o User escrever o título, vai gerar uma slug com o título
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        # nao esqueça de retornar oq está sobrescrevendo
        return super().save(*args, **kwargs)
