# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_command.py


from typing import List  # pylint: disable=W0611

from django import forms
from django.http import HttpRequest
from django.test import TestCase

from mcadmin.command import ManagementCommandAdmin
from mcadmin.forms import (
    ManagementCommandAdminFormTask,
    ManagementCommandAdminFilesForm,
)
from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = ["ManagementCommandAdminTest"]  # type: List[str]


class TestManagementCommandAdminTemplateFile(ManagementCommandAdminTemplateFile):
    """
    Management command admin example file for tests.
    """

    path = "test.csv"
    description = "Test file"


class TestManagementCommandAdminFilesTaskForm(
    ManagementCommandAdminFilesForm, ManagementCommandAdminFormTask
):
    """
    Management command admin form for tests.
    """

    path = forms.FileField(label="file", required=True)


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """
    Management command admin for tests.
    """

    command = "test-command"
    name = "Test Command"
    form = TestManagementCommandAdminFilesTaskForm
    templates = [TestManagementCommandAdminTemplateFile()]


class ManagementCommandAdminTest(TestCase):
    """
    Management commands admin tests.
    """

    def test_get_form(self):
        """
        get_form method must return form instance initialised with request data.
        """

        command = TestManagementCommandAdmin()
        request = HttpRequest()
        result = command.get_form(request=request)
        expected = TestManagementCommandAdminFilesTaskForm(
            data=request.POST, files=request.FILES
        )

        self.assertHTMLEqual(
            html1=result.as_p(), html2=expected.as_p(),  # type: ignore
        )
