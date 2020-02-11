# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/permissions/test_group.py


from typing import List, Optional  # pylint: disable=W0611

from django.contrib.auth import get_user_model
from django.test import TestCase

from mcadmin.models.group import Group
from mcadmin.models.permissions.group import CommandGroupPermission


__all__ = ["CommandGroupPermissionModelTest"]  # type: List[str]


User = get_user_model()


class CommandGroupPermissionModelTest(TestCase):
    """
    Command group permission model tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        group = Group.objects.create(name="Test")
        user = User.objects.create_user(
            username="test", password=User.objects.make_random_password()
        )
        CommandGroupPermission.objects.create(user=user, group=group)

    def test___unicode__(self):
        """
        __unicode__ method must return formatted group permission name.
        """

        group = (
            CommandGroupPermission.objects.first()
        )  # type: Optional[CommandGroupPermission]

        self.assertEqual(first=group.__unicode__(), second="Test - test")  # type: ignore  # noqa: E501

    def test___repr__(self):
        """
        __repr__ method must return formatted group permission name.
        """

        group = (
            CommandGroupPermission.objects.first()
        )  # type: Optional[CommandGroupPermission]

        self.assertEqual(first=group.__repr__(), second="Test - test")

    def test___str__(self):
        """
        __str__ method must return formatted group permission name.
        """

        group = (
            CommandGroupPermission.objects.first()
        )  # type: Optional[CommandGroupPermission]

        self.assertEqual(first=group.__str__(), second="Test - test")
