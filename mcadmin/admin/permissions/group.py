# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/permission/group.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin


__all__ = ["GroupPermissionAdmin"]  # type: List[str]


class GroupPermissionAdmin(admin.ModelAdmin):
    """
    Customize GroupPermission model for admin area.
    """

    list_display = [
        "group",
        "user",
    ]  # type: List[str]
    list_filter = [
        "group",
        "user",
    ]  # type: List[str]
    search_fields = [
        "group",
        "user__name",
    ]  # type: List[str]
