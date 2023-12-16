from django.apps import AppConfig


class HivesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hives'

    def ready(self):
        import hives.signals
