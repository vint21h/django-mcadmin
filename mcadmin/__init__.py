# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/__init__.py


from typing import List  # pylint: disable=W0611

from django.utils.module_loading import autodiscover_modules

from mcadmin.conf import settings
from mcadmin.registry import registry


__all__ = ["default_app_config", "autodiscover"]  # type: List[str]


def autodiscover() -> None:
    """
    Autodiscover management commands admins.
    """

    autodiscover_modules(settings.MCADMIN_MODULE_NAME, register_to=registry)


default_app_config = "mcadmin.apps.DjangoManagementCommandsAdminConfig"
