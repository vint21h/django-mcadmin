# -*- coding: utf-8 -*-

# django-mcadmin
# tests/test_template.py


from typing import List  # pylint: disable=W0611

from django.test import TestCase

from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = ["ManagementCommandAdminTemplateFileTest"]  # type: List[str]


class TestManagementCommandAdminTemplateFile(ManagementCommandAdminTemplateFile):
    """
    Management command admin example file for tests.
    """

    path = "test.csv"
    description = "Test file"


class ManagementCommandAdminTemplateFileTest(TestCase):
    """
    Management commands admin template file tests.
    """

    def test_get_absolute_url(self):
        """
        get_absolute_url method must return URL to template file.
        """

        template = TestManagementCommandAdminTemplateFile()

        self.assertEqual(
            first=template.get_absolute_url, second="/templates/test.csv",
        )

    def test_get_absolute_url__raw(self):
        """
        get_absolute_url method must return ful URL to template raw file.
        """

        template = TestManagementCommandAdminTemplateFile()
        template.raw = True

        self.assertEqual(
            first=template.get_absolute_url, second="test.csv",
        )
