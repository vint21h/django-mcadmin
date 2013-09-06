# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/commands.py

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mcadmin.utils import CommandsLoader

__all__ = ['ManagementCommandAdminCommand', ]


class ManagementCommandAdminCommand(models.Model):
    """
    Management commands admin command.
    """

    command = models.CharField(max_length=255, verbose_name=_(u'management command name'), choices=CommandsLoader().choices, help_text=_(u'this list get from settings'), db_index=True)
    group = models.ForeignKey('mcadmin.ManagementCommandAdminGroup', verbose_name=_(u'group'), db_index=True, related_name='commands')

    def __unicode__(self):

        return self.command

    class Meta:

        app_label = 'mcadmin'
        unique_together = ['command', 'group', ]
        verbose_name = _(u'management command')
        verbose_name_plural = _(u'management commands')
        ordering = ['command']
