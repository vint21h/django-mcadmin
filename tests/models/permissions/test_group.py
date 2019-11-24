# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/permissions/test_group.py


from typing import List, Optional  # pylint: disable=W0611

from django.contrib.auth import get_user_model
from django.test import TestCase

from mcadmin.models.group import Group
from mcadmin.models.permissions.group import GroupPermission


__all__ = ["GroupPermissionModelTest"]  # type: List[str]


User = get_user_model()


class GroupPermissionModelTest(TestCase):
    """
    Group permission model tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        user = User.objects.create(
            username="test",
            email="test@example.com",
            password=User.objects.make_random_password(),
            is_staff=True,
        )
        group = Group.objects.create(name="Test")
        GroupPermission.objects.create(group=group, user=user)

    def test___unicode__(self):
        """
        __unicode__ method must return permission group name and user name.
        """

        permission = GroupPermission.objects.first()  # type: Optional[GroupPermission]

        self.assertEqual(first=permission.__unicode__(), second="Test - test")

    def test___repr__(self):
        """
        __repr__ method must return permission group name and user name.
        """

        permission = GroupPermission.objects.first()  # type: Optional[GroupPermission]

        self.assertEqual(first=permission.__repr__(), second="Test - test")

    def test___str__(self):
        """
        __str__ method must return permission group name and user name.
        """

        permission = GroupPermission.objects.first()  # type: Optional[GroupPermission]

        self.assertEqual(first=permission.__str__(), second="Test - test")
