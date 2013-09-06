# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py

from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from annoying.decorators import render_to

from mcadmin.utils import CommandsLoader
from mcadmin.forms import ManagementCommandAdminFormWithFiles

__all__ = ['index', ]

@user_passes_test(lambda u: u.is_staff)
@render_to('mcadmin/index.html')
def index(request):
    """
    Main management commands admin view.
    """

    title = _(u'Management commands')  # need to show in page title

    loader = CommandsLoader(request=request)

    if request.method == 'POST':
        command = loader.commands[list(set(loader.commands.keys()) & set(request.POST.keys()))[0]]  # get first command from POST data

        command.form = command.form(request.POST, request.FILES)
        if command.form.is_valid():
            if isinstance(command.form, ManagementCommandAdminFormWithFiles) and command.templates:  # check if form have files
                command.form.save_files()

            try:
                command.handle(*command.form2args(request.POST), **command.form2kwargs(request.POST))
                messages.success(request, _(u"Run '%s' management command success") % command.name)
            except Exception, err:
                messages.error(request, _(u"Running '%s' management command error: %s") % (command.name, err, ))
        else:
            messages.error(request, _(u"This form was completed with errors: %s") % command.name)

    return locals()
