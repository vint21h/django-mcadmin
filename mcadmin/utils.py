# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/utils.py

from django.core.urlresolvers import reverse

__all__ = ['ManagementCommandAdminTemplateFile', ]


class ManagementCommandAdminTemplateFile(object):
    """
    Management command admin example file class.
    """

    path = u''  # path in MCADMIN_UPLOAD_TEMPLATES_PATH
    description = u''

    @property
    def get_absolute_url(self):
        """
        Return url to template file.
        """

        return reverse('mcadmin-template-file', args=[self.path, ])
