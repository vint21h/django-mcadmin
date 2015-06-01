# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/apps.py

from __future__ import unicode_literals

from django.apps import AppConfig

__all__ = ["MCAdminConfig", ]


class MCAdminConfig(AppConfig):

    name = "mcadmin"
    verbose_name = "Management commands admin"
