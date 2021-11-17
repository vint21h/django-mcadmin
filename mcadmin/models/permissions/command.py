# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions/user.py


from typing import List

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


__all__: List[str] = [
    "CommandPermission",
]


class CommandPermission(models.Model):  # noqa: DJ10,DJ11
    """User management commands admin command permission."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        db_index=True,
        related_name="commands_permissions",
        on_delete=models.CASCADE,
    )
    command = models.ForeignKey(
        "mcadmin.Command",
        verbose_name=_("command"),
        db_index=True,
        related_name="users",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Model settings."""

        app_label: str = "mcadmin"
        unique_together: List[str] = [
            "command",
            "user",
        ]
        verbose_name: str = _("management command permission")
        verbose_name_plural: str = _("management commands permissions")
        ordering: List[str] = [
            "command",
        ]

    def __str__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and user names
        :rtype: str
        """
        return self.__unicode__()

    def __unicode__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and user names
        :rtype: str
        """
        return f"{self.command} - {self.user}"

    def __repr__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and user names
        :rtype: str
        """
        return self.__unicode__()
