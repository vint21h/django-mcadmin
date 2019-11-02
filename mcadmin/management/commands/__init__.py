# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/management/commands/__init__.py


import logging
from typing import Any, Dict, List  # pylint: disable=W0611

from django.core.management.base import BaseCommand, CommandParser
from django.utils.translation import ugettext_lazy as _


__all__ = ["TaskCommand"]  # type: List[str]


class TaskCommand(BaseCommand):
    """
    Management commands admin base command class.
    Can run management command as celery task.
    """

    logger = logging.getLogger(__name__)

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command arguments.

        :param parser: command arguments parser instance.
        :type parser: django.core.management.base.CommandParser.
        :return: nothing.
        :rtype: None.
        """

        parser.add_argument(
            "--quiet",
            "-q",
            dest="quiet",
            help=_("Be quiet"),
            default=False,
            action="store_true",
            metavar="QUIET",
            type=bool,
        )
        parser.add_argument(
            "--run-as-celery-task",
            "-T",
            dest="as_task",
            help=_("Run command as celery task"),
            default=False,
            action="store_true",
            metavar="RUN-AS-CELERY-TASK",
            type=bool,
        )

    def handle(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Detect how to run command.

        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: nothing.
        :rtype: None.
        """

        if kwargs.get("as_task", False):
            try:
                self._as_task(*args, **kwargs)
            except NotImplementedError as error:
                self.logger.error(f"{error} in {self.__class__.__name__}")
        else:
            try:
                self._local(*args, **kwargs)
            except NotImplementedError as error:
                self.logger.error(f"{error} in {self.__class__.__name__}")

    def _local(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Must be implemented in child class.
        Run command locally.

        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: nothing.
        :rtype: None.
        """

        raise NotImplementedError

    def _as_task(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Must be implemented in child class.
        Run command as celery task.

        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: nothing.
        :rtype: None.
        """

        raise NotImplementedError
