from django.apps import AppConfig


class Autor5Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoR5'

    def ready(self):
        # Import signals from the 'signals' module in the 'autoR5' app
        import autoR5.signals

