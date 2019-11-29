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
    Load commands, group them and filter by permissions.
    """

    user = None
    commands = {}  # type: Dict[Union[Group, None], Dict[str, ManagementCommandAdmin]]

    def __init__(self, user) -> None:
        """
        Init loader.

        :param user: current user.
        :type user: django.contrib.auth.models.User.
        :return: nothing.
        :rtype: None.
        """

        self.user = user
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
            self.commands.update(
                {group: {}}  # TODO: filter commands in group by user permissions
            )

        if other.count():
            self.commands.update(
                {None: {}}  # TODO: filter commands by command user permissions
            )
