# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/urls.py

from django.conf.urls.defaults import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve
from django.conf import settings

# mcadmin urls
urlpatterns = patterns('mcadmin.views',
    url(r'^templates/(?P<path>.*)$', staff_member_required(serve), {'document_root': settings.MCADMIN_UPLOAD_TEMPLATES_PATH,  'show_indexes': False, }, name="mcadmin-template-file"),
)
