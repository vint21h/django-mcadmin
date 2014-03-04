# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py

import sys

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
try:
    from django.utils import six
except ImportError:
    import six

from mcadmin.settings import COMMANDS, USE_PERMISSIONS
from mcadmin.command import BaseManagementCommandAdmin
from mcadmin.models.groups import ManagementCommandAdminGroup
from mcadmin.models.permissions import ManagementCommandAdminGroupPermission


__all__ = ['ManagementCommandAdminTemplateFile', 'CommandsLoader', 'import_by_path', ]


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

        if not len(COMMANDS.keys()):
            raise ImproperlyConfigured(u'Empty MCADMIN_COMMANDS option')

        self.load()
        if USE_PERMISSIONS:  # filter commands and groups
            self.filter()

    def load(self):
        """
        Load and initialize commands from settings.
        """

        for module in COMMANDS.keys():
            for cls in COMMANDS[module]:
                command = import_by_path(u'%s.%s' % (module, cls))
                if issubclass(command, BaseManagementCommandAdmin):
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
        Filter commands and groups by permissions.
        """

        if self.request and not self.request.user.is_superuser:  # superusers get all commands list
            commands = []
            groups = []
            for group in ManagementCommandAdminGroup.objects.filter(pk__in=ManagementCommandAdminGroupPermission.objects.filter(user_group__in=self.request.user.groups.all()).values_list('group', flat=True)):
                commands += group.commands.all().values_list('command', flat=True)

            # remove commands without permissions to access to
            for command in self.commands.keys():
                if command not in commands:
                    del self.commands[command]

            # collect groups with commands with permissions to access to
            for group in self.groups:
                if group.commands.filter(command__in=self.commands.keys()).exists():
                    groups.append(group.pk)

            self.groups = ManagementCommandAdminGroup.objects.filter(pk__in=groups)


def import_by_path(dotted_path, error_prefix=''):
    """
    From Django==1.6.1, use to compatibility with old django versions.
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImproperlyConfigured if something goes wrong.
    """

    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
            error_prefix, dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as e:
        msg = '%sError importing module %s: "%s"' % (
            error_prefix, module_path, e)
        six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                    sys.exc_info()[2])
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
            error_prefix, module_path, class_name))
    return attr
