# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py


from typing import Any, Dict, List, Type  # pylint: disable=W0611

from django import forms
from django.core.management import call_command
from django.http import QueryDict


__all__ = [
    "ManagementCommandAdmin",
]  # type: List[str]


class ManagementCommandAdmin(object):
    """
    Base management command admin class.
    """

    command = ""  # type: str
    name = ""  # type: str
    args = [
        True,
    ]  # type: List[Any]
    kwargs = {}  # type: Dict[str, Any]
    form = forms.Form  # type: Type[forms.Form]
    templates = []  # type: ignore

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
