# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_example.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.example import ManagementCommandAdminExampleFile


__all__ = ["ManagementCommandAdminExampleFileTest"]  # type: List[str]


class TestManagementCommandAdminExampleFile(ManagementCommandAdminExampleFile):
    """
    Management command admin example file for tests.
    """

    path = "test.csv"
    description = "Test file"


class ManagementCommandAdminExampleFileTest(TestCase):
    """
    Management commands admin example file tests.
    """

    def test_get_absolute_url(self):
        """
        get_absolute_url method must return URL to example file.
        """

        example = TestManagementCommandAdminExampleFile()

        self.assertEqual(
            first=example.get_absolute_url,
            second="/examples/test.csv",
        )

    def test_get_absolute_url__raw(self):
        """
        get_absolute_url method must return ful URL to example raw file.
        """

        example = TestManagementCommandAdminExampleFile()
        example.raw = True

        self.assertEqual(
            first=example.get_absolute_url,
            second="test.csv",
        )
