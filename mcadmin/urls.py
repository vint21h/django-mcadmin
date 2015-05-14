# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/urls.py

from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve

from mcadmin.settings import UPLOAD_TEMPLATES_PATH
from mcadmin.views import Index

# mcadmin urls
urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='mcadmin-index'),
    url(r'^templates/(?P<path>.*)$', staff_member_required(serve), {'document_root': UPLOAD_TEMPLATES_PATH,  'show_indexes': False, }, name="mcadmin-template-file"),
)
