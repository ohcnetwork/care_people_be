from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "care_people_be"


class CarePeopleConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = _("Care people")

    def ready(self):
        import care_people_be.signals  # noqa F401
