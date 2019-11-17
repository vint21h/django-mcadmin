# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/permission/user.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin


__all__ = ["UserPermissionAdmin"]  # type: List[str]


class UserPermissionAdmin(admin.ModelAdmin):
    """
    Customize UserPermission model for admin area.
    """

    list_display = [
        "command",
        "user",
    ]  # type: List[str]
    list_filter = [
        "command",
        "user",
    ]  # type: List[str]
    search_fields = [
        "command__command",
        "user__name",
    ]  # type: List[str]
