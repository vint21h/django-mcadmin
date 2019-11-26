# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py


from typing import List  # pylint: disable=W0611

from django.urls import reverse


__all__ = [
    "ManagementCommandAdminTemplateFile",
]  # type: List[str]


class ManagementCommandAdminTemplateFile(object):
    """
    Management command admin example file class.
    """

    # path in MCADMIN_TEMPLATES_PATH (or URL for raw file)
    path = ""  # type: str
    description = ""  # type: str
    raw = False  # type: bool

    @property
    def get_absolute_url(self) -> str:
        """
        Return URL to template file.

        :return: template file URL.
        :rtype: str.
        """

        if self.raw:

            return self.path
        else:

            return reverse("mcadmin-template-file", args=[self.path])
