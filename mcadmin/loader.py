# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/loader.py


from typing import Dict, List, Union  # pylint: disable=W0611

from mcadmin.command import ManagementCommandAdmin
from mcadmin.models.group import Group


__all__ = [
    "ManagementCommandsLoader",
]  # type: List[str]


class ManagementCommandsLoader(object):
    """
    Load commands, group them and filter by permissions.
    """

    user = None
    commands = {}  # type: Dict[Union[Group, None], List[ManagementCommandAdmin]]

    def __init__(self, user) -> None:
        """
        Init loader.

        :param user: current user.
        :type user: django.contrib.auth.models.User.
        :return: nothing.
        :rtype: None.
        """

        self.user = user
        self.load()

    def load(self) -> None:
        """
        Load and initialize commands from registry.

        :return: nothing.
        :rtype: None.
        """

        pass
