# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/loader.py


from typing import Dict, List, Type, Union  # pylint: disable=W0611

from django.db.models import QuerySet

from mcadmin.command import ManagementCommandAdmin
from mcadmin.models.command import Command
from mcadmin.models.group import Group
from mcadmin.registry import registry


__all__ = [
    "ManagementCommandsLoader",
]  # type: List[str]


class ManagementCommandsLoader(object):
    """
    Load commands and group them.
    """

    commands = (
        {}
    )  # type: Dict[Union[Group, None], Dict[str, Union[ManagementCommandAdmin, None]]]
    registry = {}  # type: Dict[str, Type[ManagementCommandAdmin]]

    def __init__(self) -> None:
        """
        Init loader.

        :return: nothing.
        :rtype: None.
        """

        self.registry = registry._registry
        self.load()

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
                {
                    group: {
                        command.command: self.get_command(name=command.command)
                        for command in group.commands.all()
                    }
                }
            )

        if other.count():
            self.commands.update(
                {
                    None: {
                        command.command: self.get_command(name=command.command)
                        for command in other
                    }
                }
            )

    def get_command(self, name: str) -> Union[ManagementCommandAdmin, None]:
        """
        Get and initialize command from registry.

        :param name: command name.
        :type name: str.
        :return: initialized command.
        :rtype: Union[ManagementCommandAdmin, None].
        """

        return self.registry[name]() if name in self.registry else None
