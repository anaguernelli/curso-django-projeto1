from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'

    def ready(self, *args, **kwargs) -> None:
        # Implicitly connect signal handlers decorated with @receiver.
        import recipes.signals # noqa
        # Explicitly connect a signal handler.
        super_ready = super().ready(*args, **kwargs)

        return super_ready
