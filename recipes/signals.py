from django.db.models.signals import pre_delete
from django.dispatch import receiver

from recipes.models import Recipe

import os


# recebendo uma instância de uma recipe do jango
def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        # quando não houver um arq associado com essa instância,
        # receberá ValueError
        # FileNotFoundError tentativa de apagar um arq e ele
        # não existir
        ...


@receiver(pre_delete, sender=Recipe)
# sender é o model q tá fazendo a chamada
# instance atual q está sendo deletada
def recipe_post_signal(sender, instance, *args, **kwargs):
    # estamos garantindo que estamos trabalhando na instância antiga
    old_instance = Recipe.objects.get(pk=instance.pk)
    delete_cover(old_instance)