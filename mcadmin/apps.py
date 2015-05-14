# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/apps.py

from django.apps import AppConfig

__all__ = ['MCAdminConfig', ]


class MCAdminConfig(AppConfig):

    name = u'mcadmin'
    verbose_name = u"Management commands admin"
