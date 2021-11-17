# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/example.py


from typing import List

from django.shortcuts import resolve_url


__all__: List[str] = [
    "ManagementCommandAdminExampleFile",
]


class ManagementCommandAdminExampleFile:
    """Management command admin example file class."""

    # path in MCADMIN_EXAMPLES_PATH (or URL for raw file)
    path: str = ""
    description: str = ""
    raw: bool = False

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

            return resolve_url(to="mcadmin-example-file", **{"path": self.path})
