# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_forms.py


import os
from pathlib import Path
import tempfile
from typing import List  # pylint: disable=W0611

from django import forms
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from freezegun import freeze_time

from mcadmin.forms import ManagementCommandAdminFilesForm


__all__ = ["ManagementCommandAdminFilesFormTest"]  # type: List[str]


class TestManagementCommandAdminForm(ManagementCommandAdminFilesForm):
    """
    Management command admin form for tests.
    """

    file = forms.FileField(allow_empty_file=True)


class ManagementCommandAdminFilesFormTest(TestCase):
    """
    Management command admin form with files tests.
    """

    def setUp(self):
        """
        Set up.
        """

        self.expected = str(
            Path(tempfile.gettempdir()).joinpath(
                "TestManagementCommandAdminForm:1991-08-24 00:00:00-82241ccfdbe16cbef0abfafb2c56bd3b--test.csv"  # noqa: E501
            )
        )

        with open("tests/fixtures/test.csv", "rb") as f:
            test = File(
                file=SimpleUploadedFile(
                    name="test.csv", content=f.read(), content_type="text/csv"
                )
            )
            self.request = RequestFactory().post(
                path=reverse("mcadmin-index"), data={"file": test},
            )

    def tearDown(self):
        """
        Tear down.
        """

        try:
            os.remove(self.expected)
        except Exception:  # nosec
            pass

    @freeze_time("1991-08-24 00:00:00")
    def test_get_filepath(self):
        """
        get_filepath method must return path for file.
        """

        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        result = form.get_filepath(filename="test.csv", size=0)

        self.assertEqual(first=result, second=self.expected)

    @freeze_time("1991-08-24 00:00:00")
    def test_save_file__path_attribute(self):
        """
        save_file method must change file field "path" attribute.
        """

        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        form.is_valid()
        form.save_file(field="file")

        result = form.fields["file"].path

        self.assertEqual(first=result, second=self.expected)

    @freeze_time("1991-08-24 00:00:00")
    def test_save_file__existence(self):
        """
        save_file method must save file.
        """

        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        form.is_valid()
        form.save_file(field="file")

        result = form.fields["file"].path

        self.assertTrue(expr=Path(result).exists())

    @freeze_time("1991-08-24 00:00:00")
    def test_save_files__existence(self):
        """
        save_files method must save files.
        """

        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        form.is_valid()
        form.save_file(field="file")

        result = form.fields["file"].path

        self.assertTrue(expr=Path(result).exists())
