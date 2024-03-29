# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_command.py


from typing import List

from django.test import TestCase
from django.shortcuts import resolve_url
from django.test.client import RequestFactory

from mcadmin.command import ManagementCommandAdmin
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.forms.helpers import ManagementCommandAdminTaskForm


__all__: List[str] = ["ManagementCommandAdminTest"]


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
    """Management command admin example file for tests."""

    path: str = "test.csv"
    description: str = "Test file"


class TestManagementCommandAdminForm(ManagementCommandAdminTaskForm):
    """Management command admin form for tests."""

    ...


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """Management command admin for tests."""

    command = "test-command"
    name = "Test Command"
    form = TestManagementCommandAdminForm
    examples = [TestManagementCommandAdminExampleFile()]


class ManagementCommandAdminTest(TestCase):
    """Management commands admin tests."""

    def setUp(self) -> None:
        """Set up."""
        self.command = TestManagementCommandAdmin()
        self.request = RequestFactory().post(
            path=resolve_url(to="mcadmin-index"),
            data={
                "as_task": "on",
                "tests.test_command.TestManagementCommandAdmin": "tests.test_command.TestManagementCommandAdmin",  # noqa: E501
            },
        )

    def test_get_form(self) -> None:
        """get_form method must return form instance initialized with request data."""
        result = self.command.get_form(request=self.request)
        expected = TestManagementCommandAdminForm(
            data=self.request.POST, files=self.request.FILES
        )

        self.assertHTMLEqual(
            html1=result.as_p(),  # type: ignore
            html2=expected.as_p(),
        )

    def test_get_form_value(self) -> None:
        """get_form_value method must return form field value."""
        form = self.command.get_form(request=self.request)
        form.is_valid()  # type: ignore
        result = self.command.form_value(
            form=form, key="as_task", data=self.request.POST  # type: ignore
        )

        self.assertEqual(first=result, second="on")

    def test_form_to_args(self) -> None:
        """form_to_args method must return converted form data."""
        form = self.command.get_form(request=self.request)
        form.is_valid()  # type: ignore
        result = self.command.form_to_args(form=form, data=self.request.POST)  # type: ignore  # noqa: E501

        self.assertEqual(first=result, second=["on"])

    def test_form_to_kwargs(self) -> None:
        """form_to_kwargs method must return converted form data."""
        form = self.command.get_form(request=self.request)
        form.is_valid()  # type: ignore
        result = self.command.form_to_kwargs(form=form, data=self.request.POST)  # type: ignore  # noqa: E501

        self.assertEqual(first=result, second={"as_task": "on"})
