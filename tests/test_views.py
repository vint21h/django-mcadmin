# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_views.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from mcadmin.command import ManagementCommandAdmin
from mcadmin.forms.helpers import ManagementCommandAdminTaskForm
from mcadmin.loader import ManagementCommandsLoader
from mcadmin.models.command import Command
from mcadmin.models.group import Group
from mcadmin.registry import registry
from mcadmin.template import ManagementCommandAdminTemplateFile
from mcadmin.views import ManagementCommandsAdminIndex


__all__ = ["ManagementCommandsAdminIndexTest"]  # type: List[str]


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


class ManagementCommandsAdminIndexTest(TestCase):
    """
    Management commands admin index view tests.
    """

    def setUp(self):
        """
        Set up.
        """

        self.view = ManagementCommandsAdminIndex()
        self.request = RequestFactory().post(
            path=reverse("mcadmin-index"),
            data={
                "tests.test_views.TestManagementCommandAdmin": "tests.test_views.TestManagementCommandAdmin"  # noqa: E501
            },
        )

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        registry.register(TestManagementCommandAdmin)
        group = Group.objects.create(name="Test")
        Command.objects.create(
            command="tests.test_views.TestManagementCommandAdmin", group=group
        )

    def test_loader(self):
        """
        loader property must return commands loader.
        """

        self.assertIsInstance(obj=self.view.loader, cls=ManagementCommandsLoader)

    def test_get_context_data(self):
        """
        get_context_data method must return view context data.
        """

        expected = {
            "title": "Management commands",
            "commands": self.view.loader.commands,
            "view": self.view,
        }

        self.assertDictEqual(d1=self.view.get_context_data(), d2=expected)

    def test_get_command_name(self):
        """
        get_command_name method must return command name from request POST data.
        """

        result = self.view.get_command_name(request=self.request)
        expected = "tests.test_views.TestManagementCommandAdmin"

        self.assertEqual(first=result, second=expected)
