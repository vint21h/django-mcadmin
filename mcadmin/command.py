# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py

from django import forms
from django.core.management import call_command

from mcadmin.forms import BaseManagementCommandAdminForm

__all__ = ['BaseManagementCommandAdmin', ]


class BaseManagementCommandAdmin(object):
    """
    Base management command admin class.
    """

    command = u''
    name = u''
    args = [True, ]
    kwargs = {'quiet': True, }
    form = BaseManagementCommandAdminForm
    templates = []  # must contain instances of ManagementCommandAdminTemplateFile

    def form2kwargs(self, POST):
        """
        Serialize validated form to kwargs.
        """

        kwargs = {}

        for k in self.form.fields.keys():
            kwargs.update({k: self.value(k, POST), })

        kwargs.update(self.kwargs)  # add default options

        return kwargs

    def form2args(self, POST):
        """
        Serialize validated form to args.
        """

        args = [self.value(k, POST) for k in self.form.fields.keys()]

        return args + self.args  # add default options

    def value(self, k, POST):
        """
        Return form field value.
        """

        if isinstance(self.form.fields[k], forms.FileField):
            return self.form.fields[k].path  # for files
        else:
            return POST.get(k, None)

    def handle(self, *args, **kwargs):
        """
        Run management command.
        """

        call_command(self.command, *args, **kwargs)
