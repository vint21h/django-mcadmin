# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/registry.py


from typing import Dict, List, Type, Tuple  # pylint: disable=W0611

from mcadmin.command import ManagementCommandAdmin
from mcadmin.exceptions import (
    NotManagementCommandAdmin,
    ManagementCommandAdminNotRegistered,
    ManagementCommandAdminAlreadyRegistered,
)


__all__ = [
    "registry",
]  # type: List[str]


class ManagementCommandAdminRegistry(object):
    """
    Management commands admin registry.
    """

    _registry = {}  # type: Dict[str, Type[ManagementCommandAdmin]]

    def register(self, command) -> None:
        """
        Register management command admin.

        :param command: management command admin class.
        :type command: Type[ManagementCommandAdmin].
        :return: nothing.
        :rtype: None.
        """

        name = self.__get_command_key(command=command)

        if not issubclass(command, ManagementCommandAdmin):

            raise NotManagementCommandAdmin(
                f"The class '{name}' is not a management command admin."
            )

        if name in self._registry.keys():

            raise ManagementCommandAdminAlreadyRegistered(
                f"The command admin '{name}' is already registered."
            )

        self._registry.update({name: command})

    def unregister(self, command) -> None:
        """
        Unregister management command admin.

        :param command: management command admin class.
        :type command: Type[ManagementCommandAdmin].
        :return: nothing.
        :rtype: None.
        """

        name = self.__get_command_key(command=command)

        if not issubclass(command, ManagementCommandAdmin):

            raise NotManagementCommandAdmin(
                f"The class '{name}' is not a management command admin."
            )

        if name not in self._registry.keys():

            raise ManagementCommandAdminNotRegistered(
                f"The command admin '{name}' is not registered."
            )

        del self._registry[name]

    @staticmethod
    def __get_command_key(command) -> str:
        """
        Get command key for registry (class module name + class name).

        :param command: management command admin class.
        :type command: Type[ManagementCommandAdmin].
        :return: class module name + class name.
        :rtype: str.
        """

        return f"{command.__module__}.{command.__name__}"

    @property
    def choices(self) -> List[Tuple[str, str]]:
        """
        Get commands choices for admin.
        """

        return [(name, command.name) for name, command in self._registry.items()]


registry = ManagementCommandAdminRegistry()
