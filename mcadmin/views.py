# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py

from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from annoying.decorators import render_to

from mcadmin.utils import commands_loader

__all__ = ['index', ]

@user_passes_test(lambda u: u.is_staff)
@render_to('mcadmin/index.html')
def index(request):
    """
    Main management commands admin view.
    """

    title = _(u'Management commands')  # need to show in page title

    commands = commands_loader()

    if request.method == 'POST':
        command = commands[list(set(commands.keys()) & set(request.POST.keys()))[0]]  # get first command from POST data

        command.form = command.form(request.POST, request.FILES)
        if command.form.is_valid():
            if command.templates:
                command.form.save_files()
            try:
                command.handle(*command.form2args(request.POST), **command.form2kwargs(request.POST))
                messages.success(request, _(u"Run '%s' management command success") % command.name)
            except Exception, err:
                messages.error(request, _(u"Running '%s' management command error: %s") % (command.err, err, ))

    return locals()
