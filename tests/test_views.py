# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_views.py


from typing import List  # pylint: disable=W0611

from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.contrib.auth.models import AnonymousUser

from mcadmin.registry import registry
from mcadmin.models.group import Group
from mcadmin.models.command import Command
from mcadmin.command import ManagementCommandAdmin
from mcadmin.loader import ManagementCommandsLoader
from mcadmin.views import ManagementCommandsAdminIndex
from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.forms.helpers import ManagementCommandAdminTaskForm
from mcadmin.models.permissions.command import CommandPermission
from mcadmin.models.permissions.group import CommandGroupPermission


__all__ = ["ManagementCommandsAdminIndexTest"]  # type: List[str]


User = get_user_model()


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
    examples = [TestManagementCommandAdminExampleFile()]


class TestManagementCommandAdminInGroup(ManagementCommandAdmin):
    """
    Management command admin in group for tests.
    """

    command = "test-command-in-group"
    name = "Test Command In Group"


class ManagementCommandsAdminIndexTest(TestCase):
    """
    Management commands admin index view tests.
    """

    def setUp(self) -> None:
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
    def setUpTestData(cls) -> None:
        """
        Set up non-modified objects used by all test methods.
        """

        registry.register(TestManagementCommandAdmin)
        user = User.objects.create_user(
            username="test", password=User.objects.make_random_password()
        )
        group = Group.objects.create(name="Test")
        command = Command.objects.create(
            command="tests.test_views.TestManagementCommandAdmin"
        )
        Command.objects.create(
            command="tests.test_views.TestManagementCommandAdminInGroup", group=group
        )
        CommandGroupPermission.objects.create(user=user, group=group)
        CommandPermission.objects.create(user=user, command=command)

    def test_loader(self) -> None:
        """
        loader property must return commands loader.
        """

        self.assertIsInstance(obj=self.view.loader, cls=ManagementCommandsLoader)

    def test_get_context_data(self) -> None:
        """
        get_context_data method must return view context data.
        """

        expected = {
            "title": "Management commands",
            "COMMANDS": self.view.loader.commands,
            "view": self.view,
        }

        self.assertDictEqual(d1=self.view.get_context_data(), d2=expected)

    def test_get_command_name(self) -> None:
        """
        get_command_name method must return command name from request POST data.
        """

        result = self.view.get_command_name(request=self.request)
        expected = "tests.test_views.TestManagementCommandAdmin"

        self.assertEqual(first=result, second=expected)

    def test_filter_by_permissions__without_use_permissions(self) -> None:
        """
        filter_by_permissions method must return commands not filtered by permissions.
        """

        result = self.view.filter_by_permissions(
            commands=self.view.loader.commands, request=self.request
        )

        self.assertDictEqual(d1=result, d2=self.view.loader.commands)

    @override_settings(MCADMIN_USE_PERMISSIONS=True)
    def test_filter_by_permissions__anonymous(self) -> None:
        """
        filter_by_permissions method must not return commands.
        """

        user = AnonymousUser()

        self.request.user = user

        result = self.view.filter_by_permissions(
            commands=self.view.loader.commands, request=self.request
        )

        self.assertDictEqual(d1=result, d2={})

    @override_settings(MCADMIN_USE_PERMISSIONS=True)
    def test_filter_by_permissions__superuser(self) -> None:
        """
        filter_by_permissions method must return not filtered permissions for superuser.
        """

        user = User.objects.first()

        user.is_superuser = True  # type: ignore
        self.request.user = user  # type: ignore

        result = self.view.filter_by_permissions(
            commands=self.view.loader.commands, request=self.request
        )

        self.assertDictEqual(d1=result, d2=self.view.loader.commands)

    @override_settings(MCADMIN_USE_PERMISSIONS=True)
    def test_filter_by_permissions(self) -> None:
        """
        filter_by_permissions method must return filtered permissions.
        """

        user = User.objects.first()

        self.request.user = user  # type: ignore

        result = self.view.filter_by_permissions(
            commands=self.view.loader.commands, request=self.request
        )

        self.assertDictEqual(d1=result, d2=self.view.loader.commands)
