# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_registry.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.registry import registry
from mcadmin.command import ManagementCommandAdmin
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.exceptions import (
    NotManagementCommandAdmin,
    ManagementCommandAdminNotRegistered,
    ManagementCommandAdminAlreadyRegistered,
)


__all__ = ["ManagementCommandAdminRegistryTest"]  # type: List[str]


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


class ManagementCommandAdminRegistryTest(TestCase):
    """
    Management commands admin registry tests.
    """

    def setUp(self) -> None:
        """
        Set up.
        """

        registry.clean()

    def test_register(self) -> None:
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

    def test_register_raises_not_management_command_admin_exception(self) -> None:
        """
        register method must raise "NotManagementCommandAdmin".
        """

        with self.assertRaises(NotManagementCommandAdmin):
            registry.register(object)  # type: ignore

    def test_register_raises_management_command_admin_already_registered_exception(
        self,
    ) -> None:
        """
        register method must raise "ManagementCommandAdminAlreadyRegistered".
        """

        registry.register(TestManagementCommandAdmin)

        with self.assertRaises(ManagementCommandAdminAlreadyRegistered):
            registry.register(TestManagementCommandAdmin)

    def test_unregister(self) -> None:
        """
        unregister method must remove command from registry.
        """

        registry.register(TestManagementCommandAdmin)
        registry.unregister(TestManagementCommandAdmin)

        self.assertDictEqual(
            d1=registry._registry,
            d2={},
        )

    def test_unregister_raises_not_management_command_admin_exception(self) -> None:
        """
        unregister method must raise "NotManagementCommandAdmin".
        """

        with self.assertRaises(NotManagementCommandAdmin):
            registry.unregister(object)  # type: ignore

    def test_unregister_raises_management_command_admin_not_registered_exception(
        self,
    ) -> None:
        """
        unregister method must raise "ManagementCommandAdminNotRegistered".
        """

        with self.assertRaises(ManagementCommandAdminNotRegistered):
            registry.unregister(TestManagementCommandAdmin)

    def test__get_command_key(self) -> None:
        """
        __get_command_key method must return command class key for registry.
        """

        self.assertEqual(
            first=registry._ManagementCommandAdminRegistry__get_command_key(  # type: ignore # noqa: E501
                TestManagementCommandAdmin
            ),
            second="tests.test_registry.TestManagementCommandAdmin",
        )

    def test_choices(self) -> None:
        """
        choices property must contain commands choices for admin.
        """

        registry.register(TestManagementCommandAdmin)

        self.assertListEqual(
            list1=registry.choices,
            list2=[("tests.test_registry.TestManagementCommandAdmin", "Test Command")],
        )

    def test_clean(self) -> None:
        """
        clean method must remove all command from registry.
        """

        registry.register(TestManagementCommandAdmin)
        registry.clean()

        self.assertDictEqual(d1=registry._registry, d2={})
