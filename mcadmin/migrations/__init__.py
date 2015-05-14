# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/migrations/__init__.py


SOUTH_ERROR_MESSAGE = """\n
For South support, customize the SOUTH_MIGRATION_MODULES setting like so:

    SOUTH_MIGRATION_MODULES = {
        'mcadmin': 'mcadmin.south_migrations',
    }
"""

from django.core.exceptions import ImproperlyConfigured

# Ensure the user is not using Django 1.6 or below with South
try:
    from django.db import migrations
except ImportError:
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
