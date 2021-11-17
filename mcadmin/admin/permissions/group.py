# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/permissions/group.py


from typing import List

from django.contrib import admin


__all__: List[str] = ["CommandGroupPermissionAdmin"]


class CommandGroupPermissionAdmin(admin.ModelAdmin):  # type: ignore
    """Customize CommandGroupPermissionCommand model for admin area."""

    list_display: List[str] = [
        "user",
        "group",
    ]
    list_filter: List[str] = [
        "group",
    ]
