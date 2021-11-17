# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/registry.py


from typing import Dict, List, Type, Tuple

from mcadmin.command import ManagementCommandAdmin
from mcadmin.exceptions import (
    NotManagementCommandAdminError,
    ManagementCommandAdminNotRegisteredError,
    ManagementCommandAdminAlreadyRegisteredError,
)


__all__: List[str] = [
    "registry",
]


class ManagementCommandAdminRegistry:
    """Management commands admin registry."""

    _registry: Dict[str, Type[ManagementCommandAdmin]] = {}

    def register(self, command: Type[ManagementCommandAdmin]) -> None:
        """
        Register management command admin.

        # noqa: DAR401

        :param command: management command admin class
        :type command: Type[ManagementCommandAdmin]
        """
        name = self.__get_command_key(command=command)

        if not issubclass(command, ManagementCommandAdmin):

            raise NotManagementCommandAdminError(
                f"The class '{name}' is not a management command admin."
            )

        if name in self._registry:

            raise ManagementCommandAdminAlreadyRegisteredError(
                f"The command admin '{name}' is already registered."
            )

        self._registry.update({name: command})

    def unregister(self, command: Type[ManagementCommandAdmin]) -> None:
        """
        Unregister management command admin.

        # noqa: DAR401

        :param command: management command admin class
        :type command: Type[ManagementCommandAdmin]
        """
        name = self.__get_command_key(command=command)

        if not issubclass(command, ManagementCommandAdmin):

            raise NotManagementCommandAdminError(
                f"The class '{name}' is not a management command admin."
            )

        if name not in self._registry.keys():

            raise ManagementCommandAdminNotRegisteredError(
                f"The command admin '{name}' is not registered."
            )

        del self._registry[name]

    @staticmethod
    def __get_command_key(command) -> str:
        """
        Get command key for registry (class module name + class name).

        :param command: management command admin class
        :type command: Type[ManagementCommandAdmin]
        :return: class module name + class name
        :rtype: str
        """
        return f"{command.__module__}.{command.__name__}"

    @property
    def choices(self) -> List[Tuple[str, str]]:
        """
        Get commands choices for admin.

        :return: commands choices for admin
        :rtype: List[Tuple[str, str]]
        """
        return [(name, command.name) for name, command in self._registry.items()]

    def clean(self) -> None:
        """Clean registry."""
        self._registry = {}


registry = ManagementCommandAdminRegistry()
