"""
Imports necessary modules for configuring the 'autoR5' app.

- `AppConfig` is imported from the Django apps module and
    is used for configuring Django apps.
- `autoR5.signals` is imported to access signal definitions
    for the 'autoR5' app.
"""
from django.apps import AppConfig


class Autor5Config(AppConfig):
    """
    AppConfig class for the 'autoR5' app.

    This class represents the configuration of the 'autoR5'
    app within the Django project.
    It defines the app's name, the default auto field, and
    imports signals from the 'signals'
    module when the app is ready.

    Attributes:
        default_auto_field (str): The default auto field used
        for database models.
        name (str): The name of the 'autoR5' app.

    Methods:
        ready(self): This method is called when the app is ready
        and imports signals from the 'signals' module.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoR5'

    def ready(self):
        import autoR5.signals
