# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py


import sys
from typing import Any, Dict, List  # pylint: disable=W0611

from django.http import HttpRequest
from django.urls import reverse
from django.utils.module_loading import import_by_path

from mcadmin.command import ManagementCommandAdmin
from mcadmin.conf import settings
from mcadmin.models.group import Group
from mcadmin.models.permission import GroupPermission


__all__ = [
    "ManagementCommandAdminTemplateFile",
    "CommandsLoader",
]  # type: List[str]


class ManagementCommandAdminTemplateFile(object):
    """
    Management command admin example file class.
    """

    # path in MCADMIN_UPLOAD_TEMPLATES_PATH
    path = ""  # type: str
    description = ""  # type: str
    raw = False  # type: bool

    @property
    def get_absolute_url(self) -> str:
        """
        Return URL to template file.

        :return: template file URL.
        :rtype: str.
        """

        if self.raw:

            return self.path
        else:

            return reverse("mcadmin-template-file", args=[self.path])


class CommandsLoader(object):
    """
    Load commands and filter them by permissions.
    """

    commands = {}  # type: Dict[str, Any]
    groups = Group.objects.all()

    def __init__(self, request: HttpRequest = None) -> None:
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

    def load(self):
        """
        Load and initialize commands from settings.
        """

        for module in settings.MCADMIN_COMMANDS.keys():
            for cls in settings.MCADMIN_COMMANDS[module]:
                try:
                    command = import_by_path(f"{module}.{cls}")
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

    def filter(self):
        """
        Filter commands and groups by permissions.
        """

        if (
            self.request and not self.request.user.is_superuser
        ):  # superusers get all commands list
            commands = []
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
