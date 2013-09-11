# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/context_processors.py

from settings import USE_PERMISSIONS

__all__ = ['mcadmin']


def mcadmin(request):
    """
    mcadmin context processor.
    """

    return {'USE_PERMISSIONS': USE_PERMISSIONS, }
