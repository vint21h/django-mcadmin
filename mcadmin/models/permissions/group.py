# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions/group.py


from typing import List

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


__all__: List[str] = [
    "CommandGroupPermission",
]


class CommandGroupPermission(models.Model):  # noqa: DJ10,DJ11
    """User management commands admin group permission."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        db_index=True,
        related_name="commands_groups_permissions",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "mcadmin.Group",
        verbose_name=_("group"),
        db_index=True,
        related_name="users",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Model settings."""

        app_label: str = "mcadmin"
        unique_together: List[str] = [
            "group",
            "user",
        ]
        verbose_name: str = _("management command group permission")
        verbose_name_plural: str = _("management commands groups permissions")
        ordering: List[str] = [
            "group",
        ]

    def __str__(self) -> str:
        """
        Model representation.

        :return: formatted string with group and user names
        :rtype: str
        """
        return self.__unicode__()

    def __unicode__(self) -> str:
        """
        Model representation.

        :return: formatted string with group and user names
        :rtype: str
        """
        return f"{self.group} - {self.user}"

    def __repr__(self) -> str:
        """
        Model representation.

        :return: formatted string with group and user names
        :rtype: str
        """
        return self.__unicode__()
