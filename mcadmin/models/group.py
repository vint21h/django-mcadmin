# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/group.py


from typing import List  # pylint: disable=W0611

from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = [
    "Group",
]  # type: List[str]


class Group(models.Model):
    """
    Group for management commands admin.
    """

    name = models.CharField(max_length=255, verbose_name=_("name"), db_index=True)

    def __unicode__(self) -> str:

        return self.name

    class Meta:

        app_label = "mcadmin"  # type: str
        verbose_name = _("management commands group")  # type: str
        verbose_name_plural = _("management commands groups")  # type: str
        ordering = [
            "name",
        ]  # type: List[str]
