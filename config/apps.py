from constance.apps import ConstanceConfig
from django.utils.translation import gettext_lazy as _


class MyConstanceConfig(ConstanceConfig):
    verbose_name = _("Constance")
