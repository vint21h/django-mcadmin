# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/loader.py


from typing import Dict, List, Type, Union

from django.db.models import QuerySet

from mcadmin.registry import registry
from mcadmin.models.group import Group
from mcadmin.models.command import Command
from mcadmin.command import ManagementCommandAdmin


__all__: List[str] = [
    "ManagementCommandsLoader",
]


class ManagementCommandsLoader:
    """Load commands and group them."""

    commands: Dict[
        Union[Group, None], Dict[str, Union[ManagementCommandAdmin, None]]
    ] = {}
    registry: Dict[str, Type[ManagementCommandAdmin]] = {}

    def __init__(self) -> None:
        """Init loader."""
        self.registry = registry._registry
        self.load()

    def load(self) -> None:
        """Load and initialize commands from registry."""
        groups: QuerySet[Group] = Group.objects.filter(
            pk__in=Command.objects.all().values_list("group", flat=True)
        )
        other: QuerySet[Command] = Command.objects.filter(group__isnull=True)

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
                    None: {  # unnamed (other) group
                        command.command: self.get_command(name=command.command)
                        for command in other
                    }
                }
            )

    def get_command(self, name: str) -> Union[ManagementCommandAdmin, None]:
        """
        Get and initialize command from registry.

        :param name: command name
        :type name: str
        :return: initialized command
        :rtype: Union[ManagementCommandAdmin, None]
        """
        return self.registry[name]() if name in self.registry else None
