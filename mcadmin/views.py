# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py

from django.contrib.auth.decorators import user_passes_test

from annoying.decorators import render_to

from mcadmin.settings import COMMANDS_FILES

__all__ = ['index', ]

@user_passes_test(lambda u: u.is_staff)
@render_to('mcadmin/index.html')
def index(request):
    """
    Main management commands admin view.
    """

    commands = []

    if request.method == 'POST':
        pass

    return locals()
