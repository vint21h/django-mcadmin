# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py


import sys
from typing import Any, Dict, List, Optional  # pylint: disable=W0611

from django.http import HttpRequest
from django.utils.module_loading import import_string

from mcadmin.command import ManagementCommandAdmin
from mcadmin.conf import settings
from mcadmin.models.group import Group
from mcadmin.models.permissions.group import GroupPermission


__all__ = [
    "CommandsLoader",
]  # type: List[str]


class CommandsLoader(object):
    """
    Load commands and filter them by permissions.
    """

    commands = {}  # type: Dict[str, Any]
    groups = Group.objects.all()

    def __init__(self, request: Optional[HttpRequest] = None) -> None:
        """
        Init loader.

        :param request: request.
        :type request: HttpRequest.
        :return: nothing.
        :rtype: None.
        """

        self.request = request
        self.load()
        if settings.MCADMIN_USE_PERMISSIONS:  # filter commands and groups
            self.filter()

    def load(self) -> None:
        """
        Load and initialize commands from settings.

        :return: nothing.
        :rtype: None.
        """

        for module in settings.MCADMIN_COMMANDS.keys():
            for cls in settings.MCADMIN_COMMANDS[module]:
                try:
                    command = import_string(f"{module}.{cls}")
                    if issubclass(command, ManagementCommandAdmin):
                        command = command()
                        self.commands.update({command.command: command})
                except Exception as error:
                    sys.stderr.write(f"Could not load {module}.{cls} command. {error}")

    @property
    def choices(self):
        """
        Get commands choices for admin from commands structure.
        """

        return [(command, self.commands[command].name) for command in self.commands]

    def filter(self) -> None:
        """
        Filter commands and groups by permissions.

        :return: nothing.
        :rtype: None.
        """

        if (
            self.request and not self.request.user.is_superuser
        ):  # superusers get all commands list
            commands = []  # type: ignore
            groups = []
            for group in Group.objects.filter(
                pk__in=GroupPermission.objects.filter(
                    user_group__in=self.request.user.groups.all()
                ).values_list("group", flat=True)
            ):
                commands += group.commands.all().values_list("command", flat=True)

            # remove commands without permissions to access to
            for command in self.commands.keys():
                if command not in commands:
                    del self.commands[command]

            # collect groups with commands with permissions to access to
            for group in self.groups:
                if group.commands.filter(command__in=self.commands.keys()).exists():
                    groups.append(group.pk)

            self.groups = Group.objects.filter(pk__in=groups)
