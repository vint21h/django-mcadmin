# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/forms.py

import os
from datetime import datetime
import hashlib

from django import forms
from django.utils.translation import ugettext_lazy as _

from mcadmin.settings import UPLOADS_PATH

__all__ = ['BaseManagementCommandAdminForm', 'ManagementCommandAdminFormWithFiles', ]


class BaseManagementCommandAdminForm(forms.Form):
    """
    Management commands admin base form.
    """

    as_task = forms.BooleanField(label=_(u'Run management command as celery task'), initial=False, required=False)


class ManagementCommandAdminFormWithFiles(BaseManagementCommandAdminForm):
    """
    Management commands admin form with file upload handle.
    """

    def save_files(self):
        """
        Save all files in form.
        Must called only after form validation.
        """

        for field in self.fields:
            if isinstance(self.fields[field], forms.FileField):
                self.save_file(field)

    def save_file(self, field):
        """
        Default save file handler. May be replaced.
        But always receive field arg.
        """

        filename = u"%s:%s__%s__%s" % (self.__class__.__name__, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), hashlib.md5(u'%s%s' % (str(datetime.now()), str(self.cleaned_data['file'].size))).hexdigest(), self.cleaned_data[field])

        directory = os.path.join(UPLOADS_PATH)

        if not os.path.exists(directory):
            os.mkdir(directory)

        path = os.path.join(directory, filename)
        destination = open(path, 'wb+')
        for chunk in self.cleaned_data['file'].chunks():
            destination.write(chunk)
        destination.close()

        self.fields[field].path = path
