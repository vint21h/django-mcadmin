# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py

from __future__ import unicode_literals

import sys

from django.urls import reverse
from django.utils.module_loading import import_by_path

from mcadmin.command import BaseManagementCommandAdmin
from mcadmin.models.groups import ManagementCommandAdminGroup
from mcadmin.models.permissions import ManagementCommandAdminGroupPermission
from mcadmin.settings import COMMANDS, USE_PERMISSIONS


__all__ = [
    "ManagementCommandAdminTemplateFile",
    "CommandsLoader",
]


class ManagementCommandAdminTemplateFile(object):
    """
    Management command admin example file class.
    """

    path = ""  # path in MCADMIN_UPLOAD_TEMPLATES_PATH
    description = ""
    raw = False

    @property
    def get_absolute_url(self):
        """
        Return url to template file.
        """

        if self.raw:

            return self.path
        else:

            return reverse("mcadmin-template-file", args=[self.path,])


class CommandsLoader(object):
    """
    Load commands and filter it's by permissions.
    """

    commands = {}
    groups = ManagementCommandAdminGroup.objects.all()

    def __init__(self, request=None):
        self.request = request

        self.load()
        if USE_PERMISSIONS:  # filter commands and groups
            self.filter()

    def load(self):
        """
        Load and initialize commands from settings.
        """

        for module in COMMANDS.keys():
            for cls in COMMANDS[module]:
                try:
                    command = import_by_path(
                        "{module}.{cls}".format(module=module, cls=cls)
                    )
                    if issubclass(command, BaseManagementCommandAdmin):
                        command = command()
                        self.commands.update({command.command: command})
                except Exception as err:
                    sys.stderr.write(
                        "Couldn't load {module}.{cls} command. {err}".format(
                            module=module, cls=cls, err=err
                        )
                    )

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
            for group in ManagementCommandAdminGroup.objects.filter(
                pk__in=ManagementCommandAdminGroupPermission.objects.filter(
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

            self.groups = ManagementCommandAdminGroup.objects.filter(pk__in=groups)
