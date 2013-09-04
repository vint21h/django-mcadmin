# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/management/commands/__init__.py

from optparse import make_option
import logging

from django.core.management.base import BaseCommand

__all__ = ['TaskCommand', ]


class TaskCommand(BaseCommand):
    """
    Management commands admin base command class.
    May run management command as celery task.
    """

    logger = logging.getLogger(__name__)

    option_list = BaseCommand.option_list + (
        make_option('--quiet', '-q', dest='quiet', help=u'Be quiet', default=False, action="store_true"),
        make_option('--run-as-celery-task', '-T', dest='as_task', help=u'Run command as celery task', default=False, action="store_true"),
    )

    def handle(self, *args, **kwargs):

        if kwargs.get('as_task', False):
            try:
                self._as_task(*args, **kwargs)
            except NotImplementedError, err:
                self.logger.error(u'%s in %s' % (err, self.__class__.__name__))
                return False
        else:
            try:
                self._local(*args, **kwargs)
            except NotImplementedError, err:
                self.logger.error(u'%s in %s' % (err, self.__class__.__name__))
                return False

    def _local(self, *args, **kwargs):
        """
        Need to implement in child class.
        Run command on localhost.
        """

        raise NotImplementedError

    def _as_task(self, *args, **kwargs):
        """
        Need to implement in child class.
        Run command as celery task.
        """

        raise NotImplementedError
