# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/group.py


from typing import List, Type, Sequence  # pylint: disable=W0611

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

from mcadmin.models.command import Command


__all__ = ["GroupAdmin"]  # type: List[str]


class CommandInline(admin.TabularInline):
    """
    Command inline for GroupAdmin.
    """

    model = Command
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    """
    Customize Group model for admin area.
    """

    list_display = [
        "name",
    ]  # type: List[str]
    list_filter = [
        "name",
    ]  # type: List[str]
    search_fields = [
        "name",
    ]  # type: List[str]
    inlines = [
        CommandInline,
    ]  # type: Sequence[Type[InlineModelAdmin]]
