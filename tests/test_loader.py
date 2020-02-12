# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_loader.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.command import ManagementCommandAdmin
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.forms.helpers import ManagementCommandAdminTaskForm
from mcadmin.loader import ManagementCommandsLoader
from mcadmin.models.command import Command
from mcadmin.models.group import Group
from mcadmin.registry import registry


__all__ = ["ManagementCommandsLoaderTest"]  # type: List[str]


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
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
    examples = [ManagementCommandAdminExampleFile()]


class ManagementCommandsLoaderTest(TestCase):
    """
    Management commands loader tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        registry.register(TestManagementCommandAdmin)
        group = Group.objects.create(name="Test")
        Command.objects.create(
            command="tests.test_loader.TestManagementCommandAdmin", group=group
        )

    def test_load(self):
        """
        get_command method must return command from registry.
        """

        loader = ManagementCommandsLoader()
        group = Group.objects.first()
        result = {
            group: {
                "tests.test_loader.TestManagementCommandAdmin": loader.get_command(
                    name="tests.test_loader.TestManagementCommandAdmin"
                )
            }
        }

        self.assertDictEqual(d1=loader.commands, d2=result)

    def test_get_command(self):
        """
        get_command method must return command from registry.
        """

        loader = ManagementCommandsLoader()
        result = loader.get_command(name="tests.test_loader.TestManagementCommandAdmin")

        self.assertIsInstance(obj=result, cls=TestManagementCommandAdmin)
