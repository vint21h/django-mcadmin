# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/urls.py

from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve

from mcadmin.conf import settings
from mcadmin.views import Index


# mcadmin urls
urlpatterns = [
    url(r"^$", Index.as_view(), name="mcadmin-index"),
    url(
        r"^templates/(?P<path>.*)$",
        staff_member_required(serve),
        {
            "document_root": settings.MCADMIN_UPLOAD_TEMPLATES_PATH,
            "show_indexes": False,
        },
        name="mcadmin-template-file",
    ),
]
