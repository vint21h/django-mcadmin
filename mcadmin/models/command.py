# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/command.py


from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _

from mcadmin.registry import registry


__all__: List[str] = [
    "Command",
]


class Command(models.Model):  # noqa: DJ10,DJ11
    """Management commands admin command."""

    command = models.CharField(
        max_length=256,
        verbose_name=_("name"),
        choices=registry.choices,
        help_text=_("got from management commands admin registry"),
        db_index=True,
    )
    group = models.ForeignKey(
        "mcadmin.Group",
        verbose_name=_("group"),
        db_index=True,
        related_name="commands",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Model settings."""

        app_label: str = "mcadmin"
        unique_together: List[str] = [
            "command",
            "group",
        ]
        verbose_name: str = _("management command")
        verbose_name_plural: str = _("management commands")
        ordering: List[str] = [
            "command",
        ]

    def __str__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and group names
        :rtype: str
        """
        return self.__unicode__()

    def __unicode__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and group names
        :rtype: str
        """
        return f"{self.command} - {self.group}" if self.group else self.command

    def __repr__(self) -> str:
        """
        Model representation.

        :return: formatted string with command and group names
        :rtype: str
        """
        return self.__unicode__()
