from django.apps import AppConfig

class FlowerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flower'

    def ready(self):
        from flower import updater
        updater.start()

