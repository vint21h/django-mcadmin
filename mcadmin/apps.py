# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/apps.py


from typing import List  # pylint: disable=W0611

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


__all__ = ["DjangoManagementCommandsAdminConfig"]  # type: List[str]


class DjangoManagementCommandsAdminConfig(AppConfig):
    """
    Application config.
    """

    name = "mcadmin"
    verbose_name = _("Management commands admin")

    def ready(self) -> None:
        """
        Application ready callback.

        :return: nothing.
        :rtype: None.
        """

        super(DjangoManagementCommandsAdminConfig, self).ready()

        self.module.autodiscover()  # type: ignore
