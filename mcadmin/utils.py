# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py

import inspect

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from mcadmin.settings import COMMANDS
from mcadmin.command import BaseManagementCommandAdmin
from mcadmin.models.groups import ManagementCommandAdminGroup


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
