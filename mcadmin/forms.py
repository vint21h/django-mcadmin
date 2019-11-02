# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/forms.py


from datetime import datetime
import hashlib
import os
from typing import List  # pylint: disable=W0611

from django import forms
from django.utils.module_loading import import_by_path
from django.utils.translation import ugettext_lazy as _

from mcadmin.conf import settings


__all__ = [
    "ManagementCommandAdminFormWithTask",
    "ManagementCommandAdminFormWithFiles",
]  # type: List[str]


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

    def save_files(self) -> None:
        """
        Save all files in form.
        Must be called only after form validation.

        :return: nothing.
        :rtype: None.
        """

        for field in self.fields:
            if isinstance(self.fields[field], forms.FileField):
                self.save_file(field)

    def save_file(self, field: str) -> None:
        """
        Default save file handler. Can be overloaded.
        But always must receive field arg.

        :param field: field name.
        :type field: str.
        :return: nothing.
        :rtype: None.
        """

        path = os.path.join(  # TODO: use pathlib.
            settings.MCADMIN_UPLOADS_PATH,
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
