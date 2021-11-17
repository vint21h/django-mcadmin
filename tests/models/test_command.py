# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/test_group.py


from typing import List, Optional

from django.test import TestCase

from mcadmin.models.group import Group
from mcadmin.models.command import Command
from mcadmin.command import ManagementCommandAdmin
from mcadmin.example import ManagementCommandAdminExampleFile


__all__: List[str] = ["CommandModelTest"]


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
    """Management command admin example file for tests."""

    path: str = "test.csv"
    description: str = "Test file"


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """Management command admin for tests."""

    command: str = "test-command"
    name: str = "Test Command"
    examples: List[ManagementCommandAdminExampleFile] = [TestManagementCommandAdminExampleFile()]  # noqa: E501


class CommandModelTest(TestCase):
    """Command model tests."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up non-modified objects used by all test methods."""
        group = Group.objects.create(name="Test")
        Command.objects.create(
            command="tests.models.test_command.TestManagementCommandAdmin", group=group
        )

    def test___unicode__(self) -> None:
        """__unicode__ method must return group name."""
        command: Optional[Command] = Command.objects.first()

        self.assertEqual(
            first=command.__unicode__(),  # type: ignore
            second="tests.models.test_command.TestManagementCommandAdmin - Test",
        )

    def test___repr__(self) -> None:
        """__repr__ method must return group name."""
        command: Optional[Command] = Command.objects.first()

        self.assertEqual(
            first=command.__repr__(),
            second="tests.models.test_command.TestManagementCommandAdmin - Test",
        )

    def test___str__(self) -> None:
        """__str__ method must return group name."""
        command: Optional[Command] = Command.objects.first()

        self.assertEqual(
            first=command.__str__(),
            second="tests.models.test_command.TestManagementCommandAdmin - Test",
        )
