# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/example.py


from typing import List  # pylint: disable=W0611

from django.urls import reverse


__all__ = [
    "ManagementCommandAdminExampleFile",
]  # type: List[str]


class ManagementCommandAdminExampleFile(object):
    """
    Management command admin example file class.
    """

    # path in MCADMIN_EXAMPLES_PATH (or URL for raw file)
    path = ""  # type: str
    description = ""  # type: str
    raw = False  # type: bool

    @property
    def get_absolute_url(self) -> str:
        """
        Return URL to example file.

        :return: example file URL
        :rtype: str
        """

        if self.raw:

            return self.path
        else:

            return reverse("mcadmin-example-file", args=[self.path])
