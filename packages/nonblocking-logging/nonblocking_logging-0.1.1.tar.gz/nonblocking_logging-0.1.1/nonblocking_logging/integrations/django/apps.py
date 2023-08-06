from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .startup import start_queue_listening


class NonblockingLoggingConfig(AppConfig):
    name = "nonblocking_logging.integrations.django"
    verbose_name = _("Nonblocking Logging")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        start_queue_listening()
