from django.apps import AppConfig


class SearchengineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'searchengine'
    def ready(self):
        import searchengine.signals
