# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/test_group.py


from typing import List, Optional

from django.test import TestCase

from mcadmin.models.group import Group


__all__: List[str] = ["GroupModelTest"]


class GroupModelTest(TestCase):
    """Group model tests."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up non-modified objects used by all test methods."""
        Group.objects.create(name="Test")

    def test___unicode__(self) -> None:
        """__unicode__ method must return group name."""
        group: Optional[Group] = Group.objects.first()

        self.assertEqual(first=group.__unicode__(), second="Test")  # type: ignore

    def test___repr__(self) -> None:
        """__repr__ method must return group name."""
        group: Optional[Group] = Group.objects.first()

        self.assertEqual(first=group.__repr__(), second="Test")

    def test___str__(self) -> None:
        """__str__ method must return group name."""
        group: Optional[Group] = Group.objects.first()

        self.assertEqual(first=group.__str__(), second="Test")
