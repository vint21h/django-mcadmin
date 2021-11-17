# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py


from typing import Any, Dict, List, Union, Optional

from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test

from mcadmin.conf import settings
from mcadmin.models.group import Group
from mcadmin.command import ManagementCommandAdmin
from mcadmin.loader import ManagementCommandsLoader
from mcadmin.forms.helpers import ManagementCommandAdminFilesForm


__all__: List[str] = [
    "ManagementCommandsAdminIndex",
]


class ManagementCommandsAdminIndex(TemplateView):
    """Main management commands admin view."""

    _loader: Union[ManagementCommandsLoader, None] = None

    @method_decorator(user_passes_test(lambda user: user.is_staff))
    def dispatch(
        self, request: HttpRequest, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        """
        Overload dispatch to add staff user required checking.

        # noqa: DAR101

        :param request: request
        :type request: HttpRequest
        :param args: additional args
        :type args: List[Any]
        :param kwargs: additional args
        :type kwargs: Dict[str, Any]
        :return: dispatched request method
        :rtype: Any
        """
        return super(ManagementCommandsAdminIndex, self).dispatch(  # type: ignore
            request=request, *args, **kwargs  # type: ignore
        )

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Overload to update context.

        :param kwargs: additional args
        :type kwargs: Dict[str, Any]
        :return: updated context
        :rtype: Dict[str, Any]
        """
        context = super(ManagementCommandsAdminIndex, self).get_context_data(**kwargs)
        context.update(
            {
                "title": _("Management commands"),  # need to show in page title
                "COMMANDS": self.filter_by_permissions(
                    commands=self.loader.commands, request=kwargs.get("request")  # type: ignore  # noqa: E501
                ),
            }
        )

        return context

    def post(  # noqa: CCR001
        self, request: HttpRequest, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        """
        POST request processing.

        :param request: request
        :type request: HttpRequest
        :param args: additional args
        :type args: List[Any]
        :param kwargs: additional args
        :type kwargs: Dict[str, Any]
        :return: rendered template
        :rtype: HttpResponse
        """
        command_name = self.get_command_name(request=request)
        command = self.loader.get_command(name=command_name)

        if command:
            form = command.get_form(request=request)

            if form:
                if form.is_valid():
                    # check if form have files and save them
                    if all(
                        [
                            isinstance(form, ManagementCommandAdminFilesForm),
                            command.examples,
                        ]
                    ):
                        form.save_files()  # type: ignore
                    try:
                        command.handle(
                            **command.form_to_kwargs(form=form, data=request.POST),
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

            # some additional data for template
            kwargs.update({"COMMAND_NAME": command_name, "FORM": form})  # type: ignore

        return self.render_to_response(self.get_context_data(**kwargs))

    def get_template_names(self) -> List[str]:
        """
        Get template.

        :return: list of templates
        :rtype: List[str]
        """
        return [
            "mcadmin/index.html",
        ]

    @property
    def loader(self) -> ManagementCommandsLoader:
        """
        Get loader.

        :return: management commands loader
        :rtype: ManagementCommandsLoader
        """
        if self._loader:

            return self._loader
        else:
            self._loader = ManagementCommandsLoader()

            return self._loader

    def get_command_name(self, request: HttpRequest) -> str:
        """
        Get command name from request data.

        :param request: request
        :type request: HttpRequest
        :return: command name
        :rtype: str
        """
        commands = set(self.loader.registry).intersection(request.POST)

        return min(commands)

    @staticmethod
    def filter_by_permissions(  # noqa: CFQ004,CCR001
        commands: Dict[
            Union[Group, None], Dict[str, Union[ManagementCommandAdmin, None]]
        ],
        request: Optional[HttpRequest],
    ) -> Dict[Union[Group, None], Dict[str, Union[ManagementCommandAdmin, None]]]:
        """
        Filter commands by commands and groups permissions.

        :param commands: management commands from loader
        :type commands: Dict[Union[Group, None], Dict[str, Union[ManagementCommandAdmin, None]]]  # noqa: E501
        :param request: request
        :type request: Optional[HttpRequest]
        :return: filtered commands
        :rtype: Dict[Union[Group, None], Dict[str, Union[ManagementCommandAdmin, None]]]  # noqa: E501
        """
        if request and settings.MCADMIN_USE_PERMISSIONS:
            if request.user and request.user.is_authenticated:
                if request.user.is_superuser:

                    return commands
                else:
                    result: Dict[
                        Union[Group, None],
                        Dict[str, Union[ManagementCommandAdmin, None]],
                    ] = {}
                    groups_permissions = (
                        request.user.commands_groups_permissions.all()  # type: ignore
                        .values_list("group", flat=True)
                        .distinct()
                    )
                    commands_permissions = (
                        request.user.commands_permissions.all()  # type: ignore
                        .values_list("command__command", flat=True)
                        .distinct()
                    )

                    # filter by group permissions
                    result.update(
                        {
                            group: commands
                            for group, commands in commands.items()
                            if group and group.pk in groups_permissions
                        }
                    )
                    # filter by command permissions for commands without group
                    other = commands.get(None)
                    if commands_permissions and other:
                        result.update(
                            {
                                None: {
                                    name: command
                                    for name, command in other.items()
                                    if name in commands_permissions
                                }
                            }
                        )

                    return result
            else:

                return {}
        else:

            return commands
