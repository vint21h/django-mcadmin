# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/command.py


from typing import List, Type

from django.contrib import admin

from mcadmin.forms.admin import CommandAdminForm


__all__: List[str] = ["CommandAdmin"]


class CommandAdmin(admin.ModelAdmin):  # type: ignore
    """Customize AdminCommand model for admin area."""

    list_display: List[str] = [
        "command",
        "group",
    ]
    list_filter: List[str] = [
        "group",
    ]
    search_fields: List[str] = [
        "command",
        "group__name",
    ]
    form: Type[CommandAdminForm] = CommandAdminForm
