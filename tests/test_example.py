# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_example.py


from typing import List

from django.test import TestCase

from mcadmin.example import ManagementCommandAdminExampleFile


__all__: List[str] = ["ManagementCommandAdminExampleFileTest"]


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
    """Management command admin example file for tests."""

    path: str = "test.csv"
    description: str = "Test file"


class ManagementCommandAdminExampleFileTest(TestCase):
    """Management commands admin example file tests."""

    def test_get_absolute_url(self) -> None:
        """get_absolute_url method must return URL to example file."""
        example = TestManagementCommandAdminExampleFile()

        self.assertEqual(
            first=example.get_absolute_url,
            second="/examples/test.csv",
        )

    def test_get_absolute_url__raw(self) -> None:
        """get_absolute_url method must return ful URL to example raw file."""
        example = TestManagementCommandAdminExampleFile()
        example.raw = True

        self.assertEqual(
            first=example.get_absolute_url,
            second="test.csv",
        )
