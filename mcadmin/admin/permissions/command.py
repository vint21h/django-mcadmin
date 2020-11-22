# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/permissions/user.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin


__all__ = ["CommandPermissionAdmin"]  # type: List[str]


class CommandPermissionAdmin(admin.ModelAdmin):  # type: ignore
    """
    Customize CommandPermissionCommand model for admin area.
    """

    list_display = [
        "user",
        "command",
    ]  # type: List[str]
    list_filter = [
        "command",
    ]  # type: List[str]
