# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/settings.py

from django.conf import settings

__all__ = ['UPLOAD_TEMPLATES_PATH', 'COMMANDS_FILES', ]

UPLOAD_TEMPLATES_PATH = getattr(settings, 'MCADMIN_UPLOAD_TEMPLATES_PATH', settings.STATIC_ROOT)
COMMANDS_FILES = getattr(settings, 'MCADMIN_COMMANDS_FILES', [])
