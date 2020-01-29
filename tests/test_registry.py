# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_registry.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.command import ManagementCommandAdmin
from mcadmin.exceptions import (
    NotManagementCommandAdmin,
    ManagementCommandAdminNotRegistered,
    ManagementCommandAdminAlreadyRegistered,
)
from mcadmin.registry import registry
from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = ["ManagementCommandAdminRegistryTest"]  # type: List[str]


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


class ManagementCommandAdminRegistryTest(TestCase):
    """
    Management commands admin registry tests.
    """

    def setUp(self):
        """
        Set up.
        """

        registry.clean()

    def test_register(self):
        """
        register method must add command to registry.
        """

        registry.register(TestManagementCommandAdmin)

        self.assertDictEqual(
            d1=registry._registry,
            d2={
                "tests.test_registry.TestManagementCommandAdmin": TestManagementCommandAdmin  # noqa: E501
            },
        )

    def test_register_raises_not_management_command_admin_exception(self):
        """
        register method must raise "NotManagementCommandAdmin".
        """

        with self.assertRaises(NotManagementCommandAdmin):
            registry.register(object)

    def test_register_raises_management_command_admin_already_registered_exception(
        self,
    ):
        """
        register method must raise "ManagementCommandAdminAlreadyRegistered".
        """

        registry.register(TestManagementCommandAdmin)

        with self.assertRaises(ManagementCommandAdminAlreadyRegistered):
            registry.register(TestManagementCommandAdmin)

    def test_unregister(self):
        """
        unregister method must remove command from registry.
        """

        registry.register(TestManagementCommandAdmin)
        registry.unregister(TestManagementCommandAdmin)

        self.assertDictEqual(
            d1=registry._registry, d2={},
        )

    def test_unregister_raises_not_management_command_admin_exception(self):
        """
        unregister method must raise "NotManagementCommandAdmin".
        """

        with self.assertRaises(NotManagementCommandAdmin):
            registry.unregister(object)

    def test_unregister_raises_management_command_admin_not_registered_exception(self):
        """
        unregister method must raise "ManagementCommandAdminNotRegistered".
        """

        with self.assertRaises(ManagementCommandAdminNotRegistered):
            registry.unregister(TestManagementCommandAdmin)

    def test__get_command_key(self):
        """
        __get_command_key method must return command class key for registry.
        """

        self.assertEqual(
            first=registry._ManagementCommandAdminRegistry__get_command_key(  # type: ignore # noqa: E501
                TestManagementCommandAdmin
            ),
            second="tests.test_registry.TestManagementCommandAdmin",
        )

    def test_choices(self):
        """
        choices property must contain commands choices for admin.
        """

        registry.register(TestManagementCommandAdmin)

        self.assertListEqual(
            list1=registry.choices,
            list2=[("tests.test_registry.TestManagementCommandAdmin", "Test Command")],
        )

    def test_clean(self):
        """
        clean method must remove all command from registry.
        """

        registry.register(TestManagementCommandAdmin)
        registry.clean()

        self.assertDictEqual(d1=registry._registry, d2={})