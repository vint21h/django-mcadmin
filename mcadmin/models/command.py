# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/command.py


from typing import List  # pylint: disable=W0611

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mcadmin.command import registry


__all__ = [
    "Command",
]  # type: List[str]


class Command(models.Model):
    """
    Management commands admin command.
    """

    command = models.CharField(
        max_length=255,
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

    def __unicode__(self) -> str:

        return f"{self.command} - {self.group}"

    def __str__(self) -> str:

        return self.__unicode__()

    def __repr__(self) -> str:

        return self.__unicode__()

    class Meta:

        app_label = "mcadmin"  # type: str
        unique_together = [
            "command",
            "group",
        ]  # type: List[str]
        verbose_name = _("management command")  # type: str
        verbose_name_plural = _("management commands")  # type: str
        ordering = [
            "command",
        ]  # type: List[str]
