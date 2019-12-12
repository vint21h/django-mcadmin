# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/exceptions.py


from typing import List  # pylint: disable=W0611


__all__ = [
    "ManagementCommandAdminAlreadyRegistered",
    "ManagementCommandAdminNotRegistered",
    "NotManagementCommandAdmin",
]  # type: List[str]


class ManagementCommandAdminAlreadyRegistered(Exception):
    """
    Management command admin already registered exception.
    """

    pass  # pylint: disable=W0107


class ManagementCommandAdminNotRegistered(Exception):
    """
    Management command admin not registered exception.
    """

    pass  # pylint: disable=W0107


class NotManagementCommandAdmin(Exception):
    """
    Management command admin registry register command arg is not a management command admin exception.  # noqa: E501
    """

    pass  # pylint: disable=W0107
