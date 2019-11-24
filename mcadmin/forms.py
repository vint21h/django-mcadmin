# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/forms.py


import hashlib
import pathlib
from typing import List  # pylint: disable=W0611

from django import forms
from django.core.files.storage import DefaultStorage
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from mcadmin.conf import settings


__all__ = [
    "ManagementCommandAdminFormTask",
    "ManagementCommandAdminFormFiles",
]  # type: List[str]


class ManagementCommandAdminFormTask(forms.Form):
    """
    Management commands admin form with background task option.
    """

    as_task = forms.BooleanField(
        label=_("Run management command as background task"),
        initial=True,
        required=False,
    )


class ManagementCommandAdminFormFiles(forms.Form):
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

        filepath = self.get_filepath(
            filename=self.cleaned_data[field], size=self.cleaned_data[field].size
        )
        storage = DefaultStorage()
        storage.save(name=filepath, content=self.cleaned_data[field])  # type: ignore

        self.fields[field].path = filepath

    def get_filepath(self, filename: str, size: int) -> str:
        """
        Create unique filename under management command admin upload path.

        :param filename: original filename.
        :type filename: str.
        :param size: original file size.
        :type size: int.
        :return: unique filename under management command admin upload path.
        :rtype: str.
        """

        return str(
            pathlib.Path(settings.MCADMIN_UPLOADS_PATH).joinpath(
                "{cls}:{time}-{hash}--{file}".format(
                    cls=self.__class__.__name__,
                    time=timezone.now(),
                    hash=hashlib.md5(  # nosec
                        "{dt}{size}".format(
                            **{"dt": timezone.now(), "size": size}
                        ).encode()
                    ).hexdigest(),
                    file=filename,
                )
            )
        )
