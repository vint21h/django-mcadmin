# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/test_group.py


from typing import List, Optional  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.models.group import Group


__all__ = ["GroupModelTest"]  # type: List[str]


class GroupModelTest(TestCase):
    """
    Group model tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        Group.objects.create(name="Test")

    def test___unicode__(self):
        """
        __unicode__ method must return group name.
        """

        group = Group.objects.first()  # type: Optional[Group]

        self.assertEqual(first=group.__unicode__(), second="Test")  # type: ignore

    def test___repr__(self):
        """
        __repr__ method must return group name.
        """

        group = Group.objects.first()  # type: Optional[Group]

        self.assertEqual(first=group.__repr__(), second="Test")

    def test___str__(self):
        """
        __str__ method must return group name.
        """

        group = Group.objects.first()  # type: Optional[Group]

        self.assertEqual(first=group.__str__(), second="Test")
