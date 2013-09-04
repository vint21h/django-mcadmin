# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/forms.py

from django import forms
from django.utils.translation import ugettext_lazy as _


__all__ = ['BaseManagementCommandAdminForm', ]


class BaseManagementCommandAdminForm(forms.Form):
    """
    Management commands admin base form.
    """

    as_task = forms.BooleanField(label=_(u'Run management command as celery task'), initial=False, required=False)
