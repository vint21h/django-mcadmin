# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_loader.py


from typing import List

from django.test import TestCase

from mcadmin.registry import registry
from mcadmin.models.group import Group
from mcadmin.models.command import Command
from mcadmin.command import ManagementCommandAdmin
from mcadmin.loader import ManagementCommandsLoader
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.forms.helpers import ManagementCommandAdminTaskForm


__all__: List[str] = ["ManagementCommandsLoaderTest"]


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
    examples = [ManagementCommandAdminExampleFile()]


class ManagementCommandsLoaderTest(TestCase):
    """Management commands loader tests."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up non-modified objects used by all test methods."""
        registry.register(TestManagementCommandAdmin)
        group = Group.objects.create(name="Test")
        Command.objects.create(
            command="tests.test_loader.TestManagementCommandAdmin", group=group
        )

    def test_load(self) -> None:
        """get_command method must return command from registry."""
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

    def test_get_command(self) -> None:
        """get_command method must return command from registry."""
        loader = ManagementCommandsLoader()
        result = loader.get_command(name="tests.test_loader.TestManagementCommandAdmin")

        self.assertIsInstance(obj=result, cls=TestManagementCommandAdmin)
