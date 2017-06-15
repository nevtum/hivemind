from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DefectsConfig(AppConfig):
    name = 'dirts'
    verbose_name = _('Defects')

    def ready(self):
        from . import signals