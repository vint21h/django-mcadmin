# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models.py

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mcadmin.utils import commands_choices

__all__ = ['ManagementCommandAdminGroup', 'ManagementCommandAdminCommand', ]


class ManagementCommandAdminGroup(models.Model):
    """
    Group for management commands admin.
    """

    name = models.CharField(max_length=255, verbose_name=_(u'management commands group title'), db_index=True)

    def __unicode__(self):

        return self.name

    class Meta:

        verbose_name = _(u'management commands group')
        verbose_name_plural = _(u'management commands groups')
        ordering = ['name']

    @property
    def commands(self):
        """
        Return commands in group.
        """

        return ManagementCommandAdminCommand.objects.filter(group=self)


class ManagementCommandAdminCommand(models.Model):
    """
    Management commands admin command.
    """

    command = models.CharField(max_length=255, verbose_name=_(u'management command name'), choices=commands_choices(), help_text=_(u'this list get from settings'), db_index=True)
    group = models.ForeignKey('mcadmin.ManagementCommandAdminGroup', verbose_name=_(u'group'), db_index=True, related_name='command_group')

    def __unicode__(self):

        return self.command

    class Meta:

        unique_together = ['command', 'group', ]
        verbose_name = _(u'management command')
        verbose_name_plural = _(u'management commands')
        ordering = ['command']
