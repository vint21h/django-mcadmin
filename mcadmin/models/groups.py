# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/groups.py


from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = ['ManagementCommandAdminGroup', ]


class ManagementCommandAdminGroup(models.Model):
    """
    Group for management commands admin.
    """

    name = models.CharField(max_length=255, verbose_name=_(u'management commands group title'), db_index=True)

    def __unicode__(self):

        return self.name

    class Meta:

        app_label = 'mcadmin'
        verbose_name = _(u'management commands group')
        verbose_name_plural = _(u'management commands groups')
        ordering = ['name', ]
