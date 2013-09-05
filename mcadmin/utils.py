# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py

import inspect

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from mcadmin.settings import COMMANDS
from mcadmin.command import BaseManagementCommandAdmin


__all__ = ['ManagementCommandAdminTemplateFile', ]


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


def commands_loader():
    """
    Load and initialize commands from settings.
    """

    if not len(COMMANDS):
        raise ImproperlyConfigured(u'Empty MCADMIN_COMMANDS option')

    commands = {}
    for classes in COMMANDS:
        module = __import__(classes, fromlist=COMMANDS[classes])  # getting classes in module
        for cls in COMMANDS[classes]:
            command = getattr(module, cls)
            if inspect.isclass(command) and issubclass(command, BaseManagementCommandAdmin):  # check if it's our class
                command = command()
                commands.update({command.command: command})

    return commands


def commands_choices():
    """
    Get commands choices for admin from commands structure.
    """

    commands = commands_loader()
    choices = [(command, commands[command].name) for command in commands]

    return choices
