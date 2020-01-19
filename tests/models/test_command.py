# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/test_group.py


from typing import List, Optional  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.command import ManagementCommandAdmin
from mcadmin.models.command import Command
from mcadmin.models.group import Group
from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = ["CommandModelTest"]  # type: List[str]


class TestManagementCommandAdminTemplateFile(ManagementCommandAdminTemplateFile):
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
    templates = [TestManagementCommandAdminTemplateFile()]


class CommandModelTest(TestCase):
    """
    Command model tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        group = Group.objects.create(name="Test")
        Command.objects.create(
            command="tests.models.test_command.TestManagementCommandAdmin", group=group
        )

    def test___unicode__(self):
        """
        __unicode__ method must return group name.
        """

        command = Command.objects.first()  # type: Optional[Command]

        self.assertEqual(
            first=command.__unicode__(),  # type: ignore
            second="tests.models.test_command.TestManagementCommandAdmin - Test",
        )

    def test___repr__(self):
        """
        __repr__ method must return group name.
        """

        command = Command.objects.first()  # type: Optional[Command]

        self.assertEqual(
            first=command.__repr__(),
            second="tests.models.test_command.TestManagementCommandAdmin - Test",
        )

    def test___str__(self):
        """
        __str__ method must return group name.
        """

        command = Command.objects.first()  # type: Optional[Command]

        self.assertEqual(
            first=command.__str__(),
            second="tests.models.test_command.TestManagementCommandAdmin - Test",
        )
