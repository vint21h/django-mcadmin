# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/loader.py


from typing import Dict, List, Union  # pylint: disable=W0611

from django.db.models import QuerySet

from mcadmin.command import ManagementCommandAdmin, registry
from mcadmin.models.command import Command
from mcadmin.models.group import Group


__all__ = [
    "ManagementCommandsLoader",
]  # type: List[str]


class ManagementCommandsLoader(object):
    """
    Load commands and group them.
    """

    user = None
    commands = {}  # type: Dict[Union[Group, None], Dict[str, ManagementCommandAdmin]]

    def __init__(self) -> None:
        """
        Init loader.

        :return: nothing.
        :rtype: None.
        """

        self.load()
        self.registry = registry._registry

    def load(self) -> None:
        """
        Load and initialize commands from registry.

        :return: nothing.
        :rtype: None.
        """

        groups = Group.objects.filter(
            pk__in=Command.objects.all().values_list("group", flat=True)
        )  # type: QuerySet[Group]
        other = Command.objects.filter(group__is_null=True)  # type: QuerySet[Command]

        for group in groups:
            self.commands.update({group: {}})

        if other.count():
            self.commands.update({None: {}})
