# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions.py

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group


class ManagementCommandAdminGroupPermission(models.Model):
    """
    Management commands admin commands groups permissions.
    """

    group = models.ForeignKey("mcadmin.ManagementCommandAdminGroup", verbose_name=_("group"), db_index=True, related_name="permissions")
    user_group = models.ForeignKey(Group, verbose_name=_("user group"), db_index=True)

    def __unicode__(self):

        return "{group} - {user_group}".format(group=self.group, user_group=self.user_group)

    class Meta:

        app_label = "mcadmin"
        unique_together = ["group", "user_group", ]
        verbose_name = _("management command group permission")
        verbose_name_plural = _("management command group permissions")
        ordering = ["group", ]
