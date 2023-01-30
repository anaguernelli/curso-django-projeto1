import string
from django.db import models
from random import SystemRandom
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Aqui começam os campos para a relação genérica
    # Ex.: caso o post de onde estão comentários for apagado, esses comentários
    # Também serão apagados, por conta do on_delete com CASCADE

    # Representa o model que queremos encaixar aqui
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # Representa o id da linha do model descrito acima
    # Usa-se PositiveIntegerField caso o id seja numérico
    # Mas como nosso id pode ter letras, usaremos charfield()
    object_id = models.CharField()

    # Um campo que representa a relação genérica que conhece
    # os campos acima (contenttype e object_id)
    # GenericForeignKey() indica pro django q estamos usando um
    # campo como contentType como model e o campo object_id como id
    content_object = GenericForeignKey('content_type', 'object_id')

    # Voltando a trabalhar como model normal

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    # 5 será de forma aleatória
                    k=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Não esqueça, depois que cria ou edita um model, voce deve
# python manage.py makemigrations
# python manage.py migrate
