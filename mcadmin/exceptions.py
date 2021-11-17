# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/exceptions.py


from typing import List


__all__: List[str] = [
    "ManagementCommandAdminAlreadyRegisteredError",
    "ManagementCommandAdminNotRegisteredError",
    "NotManagementCommandAdminError",
]


class ManagementCommandAdminAlreadyRegisteredError(Exception):
    """Management command admin already registered exception."""

    ...


class ManagementCommandAdminNotRegisteredError(Exception):
    """Management command admin not registered exception."""

    ...


class NotManagementCommandAdminError(Exception):
    """Management command admin registry register command arg is not a management command admin exception."""  # noqa: E501

    ...
