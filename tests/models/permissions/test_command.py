# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/permissions/test_user.py


from typing import List, Optional  # pylint: disable=W0611

from django.test import TestCase
from django.contrib.auth import get_user_model

from mcadmin.models.command import Command
from mcadmin.command import ManagementCommandAdmin
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.models.permissions.command import CommandPermission


__all__ = ["CommandPermissionModelTest"]  # type: List[str]


User = get_user_model()


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
    """
    Management command admin example file for tests.
    """

    path = "test.csv"
    description = "Test file"


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """
    Management command admin for tests.
    """

    command = "test-command"
    name = "Test Command"
    examples = [TestManagementCommandAdminExampleFile()]


class CommandPermissionModelTest(TestCase):
    """
    Command permission model tests.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up non-modified objects used by all test methods.
        """

        user = User.objects.create_user(
            username="test", password=User.objects.make_random_password()
        )
        command = Command.objects.create(
            command="tests.models.test_command.TestManagementCommandAdmin"
        )
        CommandPermission.objects.create(user=user, command=command)

    def test___unicode__(self) -> None:
        """
        __unicode__ method must return formatted group permission name.
        """

        command = CommandPermission.objects.first()  # type: Optional[CommandPermission]
        expected = "tests.models.test_command.TestManagementCommandAdmin - test"

        self.assertEqual(first=command.__unicode__(), second=expected)  # type: ignore

    def test___repr__(self) -> None:
        """
        __repr__ method must return formatted group permission name.
        """

        command = CommandPermission.objects.first()  # type: Optional[CommandPermission]
        expected = "tests.models.test_command.TestManagementCommandAdmin - test"

        self.assertEqual(
            first=command.__repr__(),
            second=expected,
        )

    def test___str__(self) -> None:
        """
        __str__ method must return formatted group permission name.
        """

        command = CommandPermission.objects.first()  # type: Optional[CommandPermission]
        expected = "tests.models.test_command.TestManagementCommandAdmin - test"

        self.assertEqual(
            first=command.__str__(),
            second=expected,
        )
