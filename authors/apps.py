from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'

# criado o signal, precisamos definir a func ready
# ele conecta os sinais daqui
    def ready(self, *args, **kwargs) -> None:
        import authors.signals # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
