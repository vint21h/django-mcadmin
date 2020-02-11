# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/permissions/group.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin


__all__ = ["CommandGroupPermissionAdmin"]  # type: List[str]


class CommandGroupPermissionAdmin(admin.ModelAdmin):
    """
    Customize CommandGroupPermissionCommand model for admin area.
    """

    list_display = [
        "user",
        "group",
    ]  # type: List[str]
    list_filter = [
        "group",
    ]  # type: List[str]
