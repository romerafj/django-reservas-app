# reservas/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ReservasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservas'
    verbose_name = _('Reservas')

    def ready(self):
        pass  # Asegúrate de que esta sección esté vacía o contenga solo código original de la aplicación