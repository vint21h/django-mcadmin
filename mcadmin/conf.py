# -*- coding: utf-8 -*-

# django-mcadmin
# djversion/conf.py


from typing import List

from appconf import AppConf
from django.conf import settings


__all__: List[str] = ["settings"]


class DjangoDjversionAppConf(AppConf):
    """Django djversion settings."""

    EXAMPLES_PATH: str = getattr(
        settings, "MCADMIN_EXAMPLES_PATH", settings.STATIC_ROOT
    )
    UPLOADS_PATH: str = getattr(settings, "MCADMIN_UPLOADS_PATH", settings.MEDIA_ROOT)
    MODULE_NAME: str = getattr(settings, "MCADMIN_MODULE_NAME", "mcommands")
    USE_PERMISSIONS: bool = getattr(settings, "MCADMIN_USE_PERMISSIONS", False)

    class Meta:
        """Config settings."""

        prefix: str = "mcadmin"
