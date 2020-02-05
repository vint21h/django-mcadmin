# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_command.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from mcadmin.command import ManagementCommandAdmin
from mcadmin.forms.helpers import ManagementCommandAdminTaskForm
from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = ["ManagementCommandAdminTest"]  # type: List[str]


class TestManagementCommandAdminTemplateFile(ManagementCommandAdminTemplateFile):
    """
    Management command admin example file for tests.
    """

    path = "test.csv"
    description = "Test file"


class TestManagementCommandAdminForm(ManagementCommandAdminTaskForm):
    """
    Management command admin form for tests.
    """

    ...


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """
    Management command admin for tests.
    """

    command = "test-command"
    name = "Test Command"
    form = TestManagementCommandAdminForm
    templates = [TestManagementCommandAdminTemplateFile()]


class ManagementCommandAdminTest(TestCase):
    """
    Management commands admin tests.
    """

    def setUp(self):
        """
        Set up.
        """

        self.command = TestManagementCommandAdmin()
        self.request = RequestFactory().post(
            path=reverse("mcadmin-index"),
            data={
                "as_task": "on",
                "tests.test_command.TestManagementCommandAdmin": "tests.test_command.TestManagementCommandAdmin",  # noqa: E501
            },
        )

    def test_get_form(self):
        """
        get_form method must return form instance initialized with request data.
        """

        result = self.command.get_form(request=self.request)
        expected = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )

        self.assertHTMLEqual(
            html1=result.as_p(), html2=expected.as_p(),  # type: ignore
        )

    def test_get_form_value(self):
        """
        get_form_value method must return form field value.
        """

        form = self.command.get_form(request=self.request)
        form.is_valid()  # type: ignore
        result = self.command.form_value(
            form=form, key="as_task", data=self.request.POST  # type: ignore
        )

        self.assertEqual(first=result, second="on")

    def test_form_to_args(self):
        """
        form_to_args method must return converted form data.
        """

        form = self.command.get_form(request=self.request)
        form.is_valid()  # type: ignore
        result = self.command.form_to_args(form=form, data=self.request.POST)  # type: ignore  # noqa: E501

        self.assertEqual(first=result, second=["on"])

    def test_form_to_kwargs(self):
        """
        form_to_kwargs method must return converted form data.
        """

        form = self.command.get_form(request=self.request)
        form.is_valid()  # type: ignore
        result = self.command.form_to_kwargs(form=form, data=self.request.POST)  # type: ignore  # noqa: E501

        self.assertEqual(first=result, second={"as_task": "on"})
