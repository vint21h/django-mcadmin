# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions/user.py


from typing import List  # pylint: disable=W0611

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mcadmin.command import registry


__all__ = ["UserPermission"]  # type: List[str]


class UserPermission(models.Model):
    """
    Management commands admin commands user permission.
    """

    command = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        choices=registry.choices,
        help_text=_("got from management commands admin registry"),
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        db_index=True,
        on_delete=models.CASCADE,
        related_name="mcadmin_commands",
    )

    def __unicode__(self) -> str:

        return f"{self.command} - {self.user}"

    def __str__(self) -> str:

        return self.__unicode__()

    def __repr__(self) -> str:

        return self.__unicode__()

    class Meta:

        app_label = "mcadmin"  # type: str
        unique_together = [
            "command",
            "user",
        ]  # type: List[str]
        verbose_name = _("management command permission")  # type: str
        verbose_name_plural = _("management command permissions")  # type: str
        ordering = [
            "user",
        ]  # type: List[str]
