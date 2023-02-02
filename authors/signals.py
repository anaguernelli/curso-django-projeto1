from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.models import Profile


# o user models vai ser conectado a um sinal e ele vai
# emitir(receiver) um sinal quando meu perfil for criado
# conectar um model a um sinal
User = get_user_model()

# quando oq eu informar aqui, for salvo, vai emitir o sinal abaixo
# conectar o user ao post_save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        # criado perfil,
        # (authors é o campo onetoone,
        # instance a instância = atualizada)
        profile = Profile.objects.create(author=instance)
        profile.save()
