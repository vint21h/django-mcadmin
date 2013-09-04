# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/settings.py

from django.conf import settings

__all__ = ['UPLOAD_TEMPLATES_PATH', 'COMMANDS', ]

COMMANDS = getattr(settings, 'MCADMIN_COMMANDS', [])
UPLOAD_TEMPLATES_PATH = getattr(settings, 'MCADMIN_UPLOAD_TEMPLATES_PATH', settings.STATIC_ROOT)
UPLOADS_PATH = getattr(settings, 'MCADMIN_UPLOADS_PATH', settings.MEDIA_ROOT)
