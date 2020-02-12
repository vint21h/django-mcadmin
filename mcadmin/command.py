# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py


from typing import Any, Dict, List, Type, Union, Optional  # pylint: disable=W0611

from django import forms
from django.core.management import call_command
from django.http import QueryDict, HttpRequest

from mcadmin.example import ManagementCommandAdminExampleFile
from mcadmin.forms.helpers import ManagementCommandAdminFilesForm


__all__ = [
    "ManagementCommandAdmin",
]  # type: List[str]


class ManagementCommandAdmin(object):
    """
    Base management command admin class.
    """

    command = ""  # type: str
    name = ""  # type: str
    args = []  # type: List[Any]  # default options
    kwargs = {}  # type: Dict[str, Any]  # default options
    form = None  # type: Union[Type[forms.Form], None]
    examples = []  # type: List[ManagementCommandAdminExampleFile]

    def __eq__(self, other: Any) -> bool:
        """
        Not really needed, nut very useful fro testing.

        :param other: item comparing with.
        :type other: Any.
        :return: is objects equal?
        :rtype: bool.
        """

        return all(
            [
                isinstance(other, ManagementCommandAdmin),
                self.command == other.command,
                self.name == other.name,
                self.args == other.args,
                self.kwargs == other.kwargs,
                self.form == other.form,
                self.examples == other.examples,
            ]
        )

    def form_to_kwargs(self, form: forms.Form, data: QueryDict) -> Dict[str, Any]:
        """
        Convert validated form data to command kwargs.

        :param form: form instance initialized with request data.
        :type form: forms.Form.
        :param data: request data.
        :type data: QueryDict.
        :return: command kwargs.
        :rtype: Dict[str, Any].
        """

        # set default options
        kwargs = self.kwargs  # type: Dict[str, Any]

        for key in form.fields.keys():
            kwargs.update({key: self.form_value(form=form, key=key, data=data)})

        return kwargs

    def form_to_args(self, form: forms.Form, data: QueryDict) -> List[Any]:
        """
        Convert validated form data to command args.

        :param form: form instance initialized with request data.
        :type form: forms.Form.
        :param data: request data.
        :type data: QueryDict.
        :return: command args.
        :rtype: List[Any].
        """

        # set default options
        args = self.args  # type: List[Any]

        for index, key in enumerate(form.fields.keys()):
            args.insert(index, self.form_value(form=form, key=key, data=data))

        return args

    def form_value(self, form: forms.Form, key: str, data: QueryDict) -> Any:
        """
        Get form field value.

        :param form: form instance initialized with request data.
        :type form: forms.Form.
        :param key: key name.
        :type key: str.
        :param data: request data.
        :type data: QueryDict.
        :return: key value.
        :rtype: Any.
        """

        if all(
            [
                isinstance(form, ManagementCommandAdminFilesForm),
                self.examples,
                any(
                    [
                        isinstance(form.fields[key], forms.FileField),
                        isinstance(form.fields[key], forms.ImageField),
                    ]
                ),
            ]
        ):
            # return file path for file field
            return form.fields[key].path
        else:

            return data.get(key)

    def handle(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        """
        Run management command.

        :param args: additional args.
        :type args: List[Any]
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any]
        :return: command execution result.
        :rtype: Any.
        """

        return call_command(self.command, *args, **kwargs)

    def get_form(self, request: Optional[HttpRequest]) -> Union[forms.Form, None]:
        """
        Get command form instance initialized with request data.

        :param request: request.
        :type request: HttpRequest.
        :return: form instance initialized with request data or None.
        :rtype: Union[forms.Form, None].
        """

        return (
            self.form(data=request.POST, files=request.FILES)  # type: ignore  # pylint: disable=E1102  # noqa: E501
            if request
            else None
        )
