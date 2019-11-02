# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/settings.py

from __future__ import unicode_literals

from django.conf import settings


__all__ = [
    "UPLOAD_TEMPLATES_PATH",
    "COMMANDS",
    "UPLOADS_PATH",
    "USE_PERMISSIONS",
]

COMMANDS = getattr(settings, "MCADMIN_COMMANDS", {})
UPLOAD_TEMPLATES_PATH = getattr(
    settings, "MCADMIN_UPLOAD_TEMPLATES_PATH", settings.STATIC_ROOT
)
UPLOADS_PATH = getattr(settings, "MCADMIN_UPLOADS_PATH", settings.MEDIA_ROOT)
USE_PERMISSIONS = getattr(settings, "MCADMIN_USE_PERMISSIONS", False)
