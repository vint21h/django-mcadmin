# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_registry.py


from typing import List

from django.test import TestCase

from mcadmin.registry import registry
from mcadmin.command import ManagementCommandAdmin
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.exceptions import (
    NotManagementCommandAdminError,
    ManagementCommandAdminNotRegisteredError,
    ManagementCommandAdminAlreadyRegisteredError,
)


__all__: List[str] = ["ManagementCommandAdminRegistryTest"]


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
    """Management command admin example file for tests."""

    path: str = "test.csv"
    description: str = "Test file"


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """Management command admin for tests."""

    command: str = "test-command"
    name: str = "Test Command"
    examples: List[ManagementCommandAdminExampleFile] = [TestManagementCommandAdminExampleFile()]  # noqa: E501


class ManagementCommandAdminRegistryTest(TestCase):
    """Management commands admin registry tests."""

    def setUp(self) -> None:
        """Set up."""
        registry.clean()

    def test_register(self) -> None:
        """register method must add command to registry."""  # noqa: D403
        registry.register(TestManagementCommandAdmin)

        self.assertDictEqual(
            d1=registry._registry,
            d2={
                "tests.test_registry.TestManagementCommandAdmin": TestManagementCommandAdmin  # noqa: E501
            },
        )

    def test_register_raises_not_management_command_admin_exception(self) -> None:
        """register method must raise "NotManagementCommandAdminError"."""  # noqa: D403
        with self.assertRaises(NotManagementCommandAdminError):
            registry.register(object)  # type: ignore

    def test_register_raises_management_command_admin_already_registered_exception(
        self,
    ) -> None:
        """register method must raise "ManagementCommandAdminAlreadyRegisteredError"."""  # noqa: D403,E501
        registry.register(TestManagementCommandAdmin)

        with self.assertRaises(ManagementCommandAdminAlreadyRegisteredError):
            registry.register(TestManagementCommandAdmin)

    def test_unregister(self) -> None:
        """unregister method must remove command from registry."""  # noqa: D403
        registry.register(TestManagementCommandAdmin)
        registry.unregister(TestManagementCommandAdmin)

        self.assertDictEqual(
            d1=registry._registry,
            d2={},
        )

    def test_unregister_raises_not_management_command_admin_exception(self) -> None:
        """unregister method must raise "NotManagementCommandAdminError"."""  # noqa: D403,E501
        with self.assertRaises(NotManagementCommandAdminError):
            registry.unregister(object)  # type: ignore

    def test_unregister_raises_management_command_admin_not_registered_exception(
        self,
    ) -> None:
        """unregister method must raise "ManagementCommandAdminNotRegisteredError"."""  # noqa: D403,E501
        with self.assertRaises(ManagementCommandAdminNotRegisteredError):
            registry.unregister(TestManagementCommandAdmin)

    def test__get_command_key(self) -> None:
        """__get_command_key method must return command class key for registry."""
        self.assertEqual(
            first=registry._ManagementCommandAdminRegistry__get_command_key(  # type: ignore # noqa: E501
                TestManagementCommandAdmin
            ),
            second="tests.test_registry.TestManagementCommandAdmin",
        )

    def test_choices(self) -> None:
        """choices property must contain commands choices for admin."""  # noqa: D403
        registry.register(TestManagementCommandAdmin)

        self.assertListEqual(
            list1=registry.choices,
            list2=[("tests.test_registry.TestManagementCommandAdmin", "Test Command")],
        )

    def test_clean(self) -> None:
        """clean method must remove all command from registry."""  # noqa: D403
        registry.register(TestManagementCommandAdmin)
        registry.clean()

        self.assertDictEqual(d1=registry._registry, d2={})
