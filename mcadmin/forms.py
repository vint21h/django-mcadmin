# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/forms.py

from __future__ import unicode_literals

from datetime import datetime
import hashlib
import os

from django import forms
from django.conf import settings
from django.utils.module_loading import import_by_path
from django.utils.translation import ugettext_lazy as _

from mcadmin.settings import UPLOADS_PATH


__all__ = [
    "ManagementCommandAdminFormWithTask",
    "ManagementCommandAdminFormWithFiles",
]


storage = import_by_path(settings.DEFAULT_FILE_STORAGE)


class ManagementCommandAdminFormWithTask(forms.Form):
    """
    Management commands admin form with celery task option.
    """

    as_task = forms.BooleanField(
        label=_("Run management command as celery task"), initial=True, required=False
    )


class ManagementCommandAdminFormWithFiles(forms.Form):
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

        path = os.path.join(
            UPLOADS_PATH,
            "{cls}:{time}_{hash}s__{file}".format(
                cls=self.__class__.__name__,
                time=datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                hash=hashlib.md5(
                    "{dt}{size}".format(
                        dt=str(datetime.now()), size=str(self.cleaned_data[field].size)
                    )
                ).hexdigest(),
                file=self.cleaned_data[field],
            ),
        )

        upload_storage = storage()
        upload_storage.save(name=path, content=self.cleaned_data[field])

        self.fields[field].path = path
