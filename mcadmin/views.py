# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py


from typing import Any, Dict, List, Union  # pylint: disable=W0611

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from mcadmin.forms import ManagementCommandAdminFilesForm
from mcadmin.loader import ManagementCommandsLoader


__all__ = [
    "ManagementCommandsAdminIndex",
]  # type: List[str]


class ManagementCommandsAdminIndex(TemplateView):
    """
    Main management commands admin view.
    """

    _loader = None  # type: Union[ManagementCommandsLoader, None]

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

        return super(ManagementCommandsAdminIndex, self).dispatch(  # type: ignore
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
                "commands": self.loader.commands,
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

        command = self.loader.get_command(name=self.get_command_name(request=request))

        if command:
            form = command.get_form(request=request)

            if form:
                if form.is_valid():
                    if (
                        isinstance(form, ManagementCommandAdminFilesForm)
                        and command.templates
                    ):  # check if form have files and save them
                        form.save_files()
                    try:
                        command.handle(
                            *command.form_to_args(form=form, post=request.POST),
                            **command.form_to_kwargs(form=form, post=request.POST),
                        )
                        messages.success(
                            request,
                            _(f"Run '{command.name}' management command success"),
                        )
                    except Exception as error:
                        messages.error(
                            request,
                            _(
                                f"Running '{command.name}' management command error: {error}"  # noqa: E501
                            ),
                        )
                else:
                    messages.error(
                        request,
                        _(f"This form was completed with errors: {command.name}"),
                    )
            else:
                try:
                    command.handle()
                    messages.success(
                        request, _(f"Run '{command.name}' management command success"),
                    )
                except Exception as error:
                    messages.error(
                        request,
                        _(
                            f"Running '{command.name}' management command error: {error}"  # noqa: E501
                        ),
                    )

        return self.render_to_response(self.get_context_data(**kwargs))

    def get_template_names(self) -> List[str]:
        """
        Get template.

        :return: list of templates.
        :rtype: List[str].
        """

        return [
            "mcadmin/index.html",
        ]

    @property
    def loader(self) -> ManagementCommandsLoader:
        """
        Get loader.

        :return: management commands loader.
        :rtype: ManagementCommandsLoader.
        """

        if self._loader:

            return self._loader
        else:
            self._loader = ManagementCommandsLoader()

            return self._loader

    def get_command_name(self, request: HttpRequest) -> str:
        """
        Get command name from request data.

        :param request: request.
        :type request: HttpRequest.
        :return: command name.
        :rtype: str.
        """

        return min(set(self.loader.registry.keys()).intersection(request.POST.keys()))
