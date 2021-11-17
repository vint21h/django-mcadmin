# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_forms.py


import os
import tempfile
from typing import List
from pathlib import Path

from django import forms
from django.test import TestCase
from freezegun import freeze_time
from django.core.files.base import File
from django.shortcuts import resolve_url
from django.test.client import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from mcadmin.forms.helpers import ManagementCommandAdminFilesForm


__all__: List[str] = ["ManagementCommandAdminFilesFormTest"]


class TestManagementCommandAdminForm(ManagementCommandAdminFilesForm):
    """Management command admin form for tests."""

    file = forms.FileField(allow_empty_file=True)


class ManagementCommandAdminFilesFormTest(TestCase):
    """Management command admin form with files tests."""

    def setUp(self) -> None:
        """Set up."""
        self.expected = str(
            Path(tempfile.gettempdir()).joinpath(
                "uploads/TestManagementCommandAdminForm:1991-08-24 00:00:00-3cb730604796d03262c8d6c6ab7f0dd6f12b28bf2e59fe3aa566a2d0607a54a3--test.csv"  # noqa: E501
            )
        )

        with open("tests/fixtures/test.csv", "rb") as f:
            test = File(
                file=SimpleUploadedFile(
                    name="test.csv", content=f.read(), content_type="text/csv"
                )
            )
            self.request = RequestFactory().post(
                path=resolve_url(to="mcadmin-index"),
                data={"file": test},
            )

    def tearDown(self) -> None:
        """Tear down."""
        try:  # noqa: SIM105
            os.remove(self.expected)
        except Exception:  # nosec
            pass

    @freeze_time("1991-08-24 00:00:00")
    def test_get_filepath(self) -> None:
        """get_filepath method must return path for file."""
        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        result = form.get_filepath(filename="test.csv", size=0)

        self.assertEqual(first=result, second=self.expected)

    @freeze_time("1991-08-24 00:00:00")
    def test_save_file__path_attribute(self) -> None:
        """save_file method must change file field "path" attribute."""
        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        form.is_valid()
        form.save_file(field="file")

        result = form.fields["file"].path

        self.assertEqual(first=result, second=self.expected)

    @freeze_time("1991-08-24 00:00:00")
    def test_save_file__existence(self) -> None:
        """save_file method must save file."""
        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        form.is_valid()
        form.save_file(field="file")

        result = form.fields["file"].path

        self.assertTrue(expr=Path(result).exists())

    @freeze_time("1991-08-24 00:00:00")
    def test_save_files__existence(self) -> None:
        """save_files method must save files."""
        form = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )
        form.is_valid()
        form.save_file(field="file")

        result = form.fields["file"].path

        self.assertTrue(expr=Path(result).exists())
