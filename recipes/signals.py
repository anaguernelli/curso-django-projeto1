from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from recipes.models import Recipe

import os


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


# objeto de recipe é deletado quando o User deletá-lo
@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return
    # Ex.: foi colocada uma imagem num campo antes vazio,
    # O user decide trocá_la ou editá-la. A primeira img seria
    # o old_instance e a imagem atual o instance.cover
    # Portanto, se é um cover novo, deve ser a 1 img diferente
    # Da 2 colocada
    is_new_cover = old_instance != instance.cover

    if is_new_cover:
        # vai apagar do nosso bd a imagem retirada
        delete_cover(old_instance)
