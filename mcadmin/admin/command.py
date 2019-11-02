# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/command.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin


__all__ = ["CommandAdmin"]  # type: List[str]


class CommandAdmin(admin.ModelAdmin):
    """
    Customize AdminCommand model for admin area.
    """

    list_display = [
        "command",
        "group",
    ]  # type: List[str]
    list_filter = [
        "group",
    ]  # type: List[str]
    search_fields = [
        "command",
        "group__name",
    ]  # type: List[str]
