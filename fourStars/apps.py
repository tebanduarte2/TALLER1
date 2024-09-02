from django.apps import AppConfig


class FourstarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fourStars'
    
    def ready(self):
        import fourStars.signals

