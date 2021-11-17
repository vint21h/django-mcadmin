# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/permissions/user.py


from typing import List

from django.contrib import admin


__all__: List[str] = ["CommandPermissionAdmin"]


class CommandPermissionAdmin(admin.ModelAdmin):  # type: ignore
    """Customize CommandPermissionCommand model for admin area."""

    list_display: List[str] = [
        "user",
        "command",
    ]
    list_filter: List[str] = [
        "command",
    ]
