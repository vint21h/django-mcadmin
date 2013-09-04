# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py

from django.core.management import call_command

from mcadmin.forms import BaseManagementCommandAdminForm

__all__ = ['BaseManagementCommandAdmin', ]


class BaseManagementCommandAdmin(object):
    """
    Base management command admin class.
    """

    command = u''
    name = u''
    args = []
    kwargs = {'quiet': True, }
    form = BaseManagementCommandAdminForm
    templates = []  # must contain instances of ManagementCommandAdminTemplateFile

    def form2kwargs(self, form, POST):
        """
        Serialize validated form to kwargs.
        """

        kwargs = {}

        for k in form.fields.keys():
            kwargs.update({k: POST.get(k, None)})

        kwargs.update(self.kwargs)  # add default options

        return kwargs

    def form2args(self, form, POST):
        """
        Serialize validated form to args.
        """

        args = [POST.get(k, None) for k in form.fields.keys()]

        return args + self.args  # add default options

    def handle(self, *args, **kwargs):
        """
        Run management command.
        """

        call_command(self.command, *args, **kwargs)
