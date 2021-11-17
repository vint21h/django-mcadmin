# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/permissions/test_group.py


from typing import List, Optional

from django.test import TestCase
from django.contrib.auth import get_user_model

from mcadmin.models.group import Group
from mcadmin.models.permissions.group import CommandGroupPermission


__all__: List[str] = ["CommandGroupPermissionModelTest"]


User = get_user_model()


class CommandGroupPermissionModelTest(TestCase):
    """Command group permission model tests."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up non-modified objects used by all test methods."""
        group = Group.objects.create(name="Test")
        user = User.objects.create_user(
            username="test", password=User.objects.make_random_password()
        )
        CommandGroupPermission.objects.create(user=user, group=group)

    def test___unicode__(self) -> None:
        """__unicode__ method must return formatted group permission name."""
        group: Optional[CommandGroupPermission] = (
            CommandGroupPermission.objects.first()
        )

        self.assertEqual(first=group.__unicode__(), second="Test - test")  # type: ignore  # noqa: E501

    def test___repr__(self) -> None:
        """__repr__ method must return formatted group permission name."""
        group: Optional[CommandGroupPermission] = (
            CommandGroupPermission.objects.first()
        )

        self.assertEqual(first=group.__repr__(), second="Test - test")

    def test___str__(self) -> None:
        """__str__ method must return formatted group permission name."""
        group: Optional[CommandGroupPermission] = (
            CommandGroupPermission.objects.first()
        )

        self.assertEqual(first=group.__str__(), second="Test - test")
