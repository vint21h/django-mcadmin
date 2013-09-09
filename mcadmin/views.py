# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py

from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.generic import TemplateView

from mcadmin.utils import CommandsLoader
from mcadmin.forms import ManagementCommandAdminFormWithFiles

__all__ = ['Index', ]


class Index(TemplateView):
    """
    Main management commands admin view.
    """

    template_name = "mcadmin/index.html"
    loader = None

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):

        return super(Index, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(Index, self).get_context_data(**kwargs)
        context['title'] = _(u'Management commands')  # need to show in page title
        context['loader'] = self.get_loader(self.request)

        return context

    def get_loader(self, request):

        if not self.loader:
            self.loader = CommandsLoader(request=request)

        return self.loader

    def post(self, request, *args, **kwargs):

        command = self.get_loader(request).commands[list(set(self.get_loader(request).commands.keys()) & set(request.POST.keys()))[0]]  # get first command from POST data
        command.form = command.form(request.POST, request.FILES)

        if command.form.is_valid():
            if isinstance(command.form, ManagementCommandAdminFormWithFiles) and command.templates:  # check if form have files
                command.form.save_files()
            try:
                command.handle(*command.form2args(request.POST), **command.form2kwargs(request.POST))
                messages.success(request, _(u"Run '%s' management command success") % command.name)
            except Exception, err:
                messages.error(request, _(u"Running '%(name)s' management command error: %(err)s") % {'name': command.name, 'err': err, })
        else:
            messages.error(request, _(u"This form was completed with errors: %(name)s") % {'name': command.name, })

        return self.render_to_response(self.get_context_data(**kwargs))
