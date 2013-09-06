# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py

import inspect

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from mcadmin.settings import COMMANDS
from mcadmin.command import BaseManagementCommandAdmin
from mcadmin.models.groups import ManagementCommandAdminGroup
from mcadmin.models.permissions import ManagementCommandAdminGroupPermission


__all__ = ['ManagementCommandAdminTemplateFile', 'CommandsLoader', ]


class ManagementCommandAdminTemplateFile(object):
    """
    Management command admin example file class.
    """

    path = u''  # path in MCADMIN_UPLOAD_TEMPLATES_PATH
    description = u''

    @property
    def get_absolute_url(self):
        """
        Return url to template file.
        """

        return reverse('mcadmin-template-file', args=[self.path, ])


class CommandsLoader(object):
    """
    Load commands and filter it's by permissions.
    """

    commands = {}
    groups = ManagementCommandAdminGroup.objects.all()

    def __init__(self, request=None):
        self.request = request

        if not len(COMMANDS):
            raise ImproperlyConfigured(u'Empty MCADMIN_COMMANDS option')

        self.load()
        self.filter()

    def load(self):
        """
        Load and initialize commands from settings.
        """

        for classes in COMMANDS:
            module = __import__(classes, fromlist=COMMANDS[classes])  # getting classes in module
            for cls in COMMANDS[classes]:
                command = getattr(module, cls)
                if inspect.isclass(command) and issubclass(command, BaseManagementCommandAdmin):  # check if it's our class
                    command = command()
                    self.commands.update({command.command: command})

    @property
    def choices(self):
        """
        Get commands choices for admin from commands structure.
        """

        return [(command, self.commands[command].name) for command in self.commands]

    def filter(self):
        """
        Filter commands by permissions.
        """

        if self.request and not self.request.user.is_superuser:  # superusers get all commands list
            commands = []
            for group in ManagementCommandAdminGroup.objects.filter(pk__in=ManagementCommandAdminGroupPermission.objects.filter(user_group__in=self.request.user.groups.all()).values_list('group', flat=True)):
                commands += group.commands.all().values_list('command', flat=True)

            # remove commands without permissions to access to
            for command in self.commands.keys():
                if command not in commands:
                    del self.commands[command]
