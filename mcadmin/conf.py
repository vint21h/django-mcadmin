# -*- coding: utf-8 -*-

# django-mcadmin
# djversion/conf.py


from typing import Dict, List  # pylint: disable=W0611

from appconf import AppConf
from django.conf import settings


__all__ = ["settings"]  # type: List[str]


class DjangoDjversionAppConf(AppConf):
    """
    Django djversion settings.
    """

    COMMANDS = getattr(settings, "MCADMIN_COMMANDS", {})  # type: Dict[str, str]
    UPLOAD_TEMPLATES_PATH = getattr(
        settings, "MCADMIN_UPLOAD_TEMPLATES_PATH", settings.STATIC_ROOT
    )  # type: str
    UPLOADS_PATH = getattr(
        settings, "MCADMIN_UPLOADS_PATH", settings.MEDIA_ROOT
    )  # type: str
    USE_PERMISSIONS = getattr(settings, "MCADMIN_USE_PERMISSIONS", False)  # type: bool

    class Meta:

        prefix = "mcadmin"  # type: str
