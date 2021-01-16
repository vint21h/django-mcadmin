# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions/user.py


from typing import List  # pylint: disable=W0611

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


__all__ = [
    "CommandPermission",
]  # type: List[str]


class CommandPermission(models.Model):
    """
    User management commands admin command permission.
    """

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

    def __unicode__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and user names
        :rtype: str
        """

        return f"{self.command} - {self.user}"

    def __str__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and user names
        :rtype: str
        """

        return self.__unicode__()

    def __repr__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and user names
        :rtype: str
        """

        return self.__unicode__()

    class Meta:
        """
        Model settings.
        """

        app_label = "mcadmin"  # type: str
        unique_together = [
            "command",
            "user",
        ]  # type: List[str]
        verbose_name = _("management command permission")  # type: str
        verbose_name_plural = _("management commands permissions")  # type: str
        ordering = [
            "command",
        ]  # type: List[str]
