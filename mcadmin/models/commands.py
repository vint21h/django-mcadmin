# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/commands.py

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mcadmin.utils import CommandsLoader

__all__ = ["ManagementCommandAdminCommand", ]


class ManagementCommandAdminCommand(models.Model):
    """
    Management commands admin command.
    """

    command = models.CharField(max_length=255, verbose_name=_("management command name"), choices=CommandsLoader().choices, help_text=_("this list get from settings"), db_index=True)
    group = models.ForeignKey("mcadmin.ManagementCommandAdminGroup", verbose_name=_("group"), db_index=True, related_name="commands")

    def __unicode__(self):

        return "{command} - {groups}".format(command=self.command, group=self.group)

    class Meta:

        app_label = "mcadmin"
        unique_together = ["command", "group", ]
        verbose_name = _("management command")
        verbose_name_plural = _("management commands")
        ordering = ["command", ]
