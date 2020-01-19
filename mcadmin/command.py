# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/command.py


from typing import Any, Dict, List, Type, Union, Optional  # pylint: disable=W0611

from django import forms
from django.core.management import call_command
from django.http import QueryDict, HttpRequest

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
    form = None  # type: Union[Type[forms.Form], None]
    templates = []  # type: List[ManagementCommandAdminTemplateFile]

    def form_to_kwargs(self, form: forms.Form, post: QueryDict) -> Dict[str, Any]:
        """
        Convert validated form data to command kwargs.

        :param form: form instance initialised with request data.
        :type post: forms.Form.
        :param post: request POST data.
        :type post: QueryDict.
        :return: command kwargs.
        :rtype: Dict[str, Any].
        """

        kwargs = {}  # type: Dict[str, Any]

        for key in self.form.fields.keys():  # type: ignore
            kwargs.update({key: self.value(form=form, key=key, post=post)})
        kwargs.update(self.kwargs)  # add default options

        return kwargs

    def form_to_args(self, form: forms.Form, post: QueryDict) -> List[Any]:
        """
        Convert validated form data to command args.

        :param form: form instance initialised with request data.
        :type post: forms.Form.
        :param post: request POST data.
        :type post: QueryDict.
        :return: command args.
        :rtype: List[Any].
        """

        args = [
            self.value(form=form, key=key, post=post) for key in form.fields.keys()
        ]  # type: List[Any]
        args.extend(self.args)  # add default options

        return args

    @staticmethod
    def value(form: forms.Form, key: str, post: QueryDict) -> Any:
        """
        Get form field value.

        :param form: form instance initialised with request data.
        :type post: forms.Form.
        :param key: key name.
        :type key: str.
        :param post: request POST data.
        :type post: QueryDict.
        :return: key value.
        :rtype: Any.
        """

        if any(
            [
                isinstance(form.fields[key], forms.FileField),
                isinstance(form.fields[key], forms.ImageField),
            ]
        ):
            # return file path for file field
            return form.fields[key].path
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

    def get_form(self, request: Optional[HttpRequest]) -> Union[forms.Form, None]:
        """
        Get command form instance initialised with request data.

        :param request: request.
        :type request: HttpRequest.
        :return: form instance initialised with request data.
        :rtype: Union[forms.Form, None].
        """

        return (
            self.form(data=request.POST, files=request.FILES)  # type: ignore  # pylint: disable=E1102  # noqa: E501
            if request
            else None
        )
