# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py


from typing import Any, Dict, List, Type, Union  # pylint: disable=W0611

from django import forms
from django.core.management import call_command
from django.http import QueryDict

from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = [
    "ManagementCommandAdmin",
]  # type: List[str]


class ManagementCommandAdmin(object):
    """
    Base management command admin class.
    """

    command = ""  # type: str
    name = ""  # type: str
    args = []  # type: List[Any]
    kwargs = {}  # type: Dict[str, Any]
    form = None  # type: Union[Type[forms.Form], forms.Form, None]
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

        for key in self.form.fields.keys():  # type: ignore
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
            self.value(key, post) for key in self.form.fields.keys()  # type: ignore
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
                isinstance(self.form.fields[key], forms.FileField),  # type: ignore
                isinstance(self.form.fields[key], forms.ImageField),  # type: ignore
            ]
        ):
            # return file path for file field
            return self.form.fields[key].path  # type: ignore
        else:

            return post.get(key)

    def handle(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Run management command.

        :param args: additional args.
        :type args: List[Any]
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any]
        :return: nothing.
        :rtype: None.
        """

        call_command(self.command, *args, **kwargs)
