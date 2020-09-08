# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions/group.py


from typing import List  # pylint: disable=W0611

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


__all__ = [
    "CommandGroupPermission",
]  # type: List[str]


class CommandGroupPermission(models.Model):
    """
    User management commands admin group permission.
    """

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

    def __unicode__(self) -> str:
        """
        Model representation.

        :return: formatted string with group and user names
        :rtype: str
        """

        return f"{self.group} - {self.user}"

    def __str__(self) -> str:
        """
        Model representation.

        :return: formatted string with group and user names
        :rtype: str
        """

        return self.__unicode__()

    def __repr__(self) -> str:
        """
        Model representation.

        :return: formatted string with group and user names
        :rtype: str
        """

        return self.__unicode__()

    class Meta:
        """
        Model settings.
        """

        app_label = "mcadmin"  # type: str
        unique_together = [
            "group",
            "user",
        ]  # type: List[str]
        verbose_name = _("management command group permission")  # type: str
        verbose_name_plural = _("management commands groups permissions")  # type: str
        ordering = [
            "group",
        ]  # type: List[str]
