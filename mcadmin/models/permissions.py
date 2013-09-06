# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions.py

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group


class ManagementCommandAdminGroupPermission(models.Model):
    """
    Management commands admin commands groups permissions.
    """

    group = models.ForeignKey('mcadmin.ManagementCommandAdminGroup', verbose_name=_(u'group'), db_index=True, related_name='permissions')
    user_group = models.ForeignKey(Group, verbose_name=_(u'user group'), db_index=True)

    def __unicode__(self):

        return u"%s - %s" % (self.group, self.user_group)

    class Meta:

        app_label = 'mcadmin'
        unique_together = ['group', 'user_group', ]
        verbose_name = _(u'management command group permission')
        verbose_name_plural = _(u'management command group permissions')
        ordering = ['group', ]
