# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py


from typing import Any, Dict, List  # pylint: disable=W0611

from django import forms  # pylint: disable=W0611
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from mcadmin.forms import ManagementCommandAdminFormWithFiles
from mcadmin.utils import CommandsLoader


__all__ = [
    "ManagementCommandsAdminIndex",
]  # type: List[str]


class ManagementCommandsAdminIndex(TemplateView):
    """
    Main management commands admin view.
    """

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> Any:
        """
        Overload dispatch to add staff user required checking.

        :param request: request.
        :type request: HttpRequest.
        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: dispatched request method.
        :rtype: Any.
        """

        return super(ManagementCommandsAdminIndex, self).dispatch(
            request=request, *args, **kwargs
        )

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Overload to update context.

        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: updated context.
        :rtype: Dict[str, Any].
        """

        context = super(ManagementCommandsAdminIndex, self).get_context_data(**kwargs)
        context.update(
            {
                "title": _("Management commands"),  # need to show in page title,
                "loader": self.loader(request=self.request),
            }
        )

        return context

    def post(
        self, request: HttpRequest, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        """
        POST request processing.

        :param request: request.
        :type request: HttpRequest.
        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: rendered template.
        :rtype: HttpResponse.
        """

        command = self.loader(request=request).commands[
            list(set(self.loader(request).commands.keys()) & set(request.POST.keys()))[
                0
            ]
        ]  # get first command from POST data
        command.form = command.form(
            data=request.POST, files=request.FILES
        )  # type: forms.Form

        if command.form.is_valid():
            if (
                isinstance(command.form, ManagementCommandAdminFormWithFiles)
                and command.templates
            ):  # check if form have files
                command.form.save_files()
            try:
                command.handle(
                    *command.form2args(post=request.POST),
                    **command.form2kwargs(post=request.POST),
                )
                messages.success(
                    request, _(f"Run '{command.name}' management command success"),
                )
            except Exception as error:
                messages.error(
                    request,
                    _(f"Running '{command.name}' management command error: {error}"),
                )
        else:
            messages.error(
                request, _(f"This form was completed with errors: {command.name}"),
            )

        return self.render_to_response(self.get_context_data(**kwargs))

    @staticmethod
    def loader(request: HttpRequest) -> CommandsLoader:
        """
        Get loader.

        :param request: request.
        :type request: HttpRequest.
        :return: commands loader.
        :rtype: CommandsLoader.
        """

        return CommandsLoader(request=request)

    def get_template_names(self) -> List[str]:
        """
        Get template.

        :return: list of templates.
        :rtype: List[str].
        """

        return [
            "mcadmin/index.html",
        ]
