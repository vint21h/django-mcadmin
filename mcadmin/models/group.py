# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/group.py


from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


__all__: List[str] = [
    "Group",
]


class Group(models.Model):  # noqa: DJ10,DJ11
    """Group for management commands admin."""

    name = models.CharField(max_length=256, verbose_name=_("name"), db_index=True)

    class Meta:
        """Model settings."""

        app_label: str = "mcadmin"
        verbose_name: str = _("management commands group")
        verbose_name_plural: str = _("management commands groups")
        ordering: List[str] = [
            "name",
        ]

    def __str__(self) -> str:
        """
        Model representation.

        :return: formatted string with group name
        :rtype: str
        """
        return self.__unicode__()

    def __unicode__(self) -> str:
        """
        Model representation.

        :return: formatted string with group name
        :rtype: str
        """
        return self.name

    def __repr__(self) -> str:
        """
        Model representation.

        :return: formatted string with group name
        :rtype: str
        """
        return self.__unicode__()
