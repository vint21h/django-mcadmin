# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py


from typing import Any, Dict, List, Type, Tuple  # pylint: disable=W0611

from django import forms
from django.core.management import call_command
from django.http import QueryDict

from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = [
    "ManagementCommandAdmin",
    "registry",
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


class ManagementCommandAdmin(object):
    """
    Base management command admin class.
    """

    command = ""  # type: str
    name = ""  # type: str
    args = []  # type: List[Any]
    kwargs = {}  # type: Dict[str, Any]
    form = forms.Form  # type: Type[forms.Form]
    templates = []  # type: List[ManagementCommandAdminTemplateFile]

    def form_to_kwargs(self, post: QueryDict) -> Dict[str, Any]:
        """
        Convert validated form data to command kwargs.

        :param post: request POST data.
        :type post: QueryDict.
        :return: command kwargs.
        :rtype: Dict[str, Any].
        """

        kwargs = {}  # type: Dict[str, Any]

        for key in self.form.fields.keys():
            kwargs.update({key: self.value(key, post)})
        kwargs.update(self.kwargs)  # add default options

        return kwargs

    def form_to_args(self, post: QueryDict) -> List[Any]:
        """
        Convert validated form data to command args.

        :param post: request POST data.
        :type post: QueryDict.
        :return: command args.
        :rtype: List[Any].
        """

        args = [
            self.value(key, post) for key in self.form.fields.keys()
        ]  # type: List[Any]
        args.extend(self.args)  # add default options

        return args

    def value(self, key: str, post: QueryDict) -> Any:
        """
        Get form field value.

        :param key: key name.
        :type key: str.
        :param post: request POST data.
        :type post: QueryDict.
        :return: key value.
        :rtype: Any.
        """

        if any(
            [
                isinstance(self.form.fields[key], forms.FileField),
                isinstance(self.form.fields[key], forms.ImageField),
            ]
        ):
            # return file path for file field
            return self.form.fields[key].path
        else:

            return post.get(key, None)

    def handle(self, *args, **kwargs):
        """
        Run management command.
        """

        call_command(self.command, *args, **kwargs)


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

    @property
    def registry(self) -> Dict[str, List[ManagementCommandAdmin]]:
        """
        Return initialized management commands admin classes.

        :return: initialized management commands admin classes.
        :rtype: Dict[str, List[ManagementCommandAdmin]].
        """

        return {}


registry = ManagementCommandAdminRegistry()
