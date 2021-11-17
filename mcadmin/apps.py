# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/apps.py


from typing import List

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


__all__: List[str] = ["DjangoManagementCommandsAdminConfig"]


class DjangoManagementCommandsAdminConfig(AppConfig):
    """Application config."""

    name: str = "mcadmin"
    verbose_name: str = _("Management commands admin")

    def ready(self) -> None:
        """Application ready callback."""
        super(DjangoManagementCommandsAdminConfig, self).ready()

        self.module.autodiscover()  # type: ignore
