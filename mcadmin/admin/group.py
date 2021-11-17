# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/group.py


from typing import List, Type, Sequence

from django.contrib import admin

from mcadmin.models.command import Command


__all__: List[str] = ["GroupAdmin"]


class CommandInline(admin.TabularInline):  # type: ignore
    """Command inline for GroupAdmin."""

    model: Type[Command] = Command
    extra: int = 1


class GroupAdmin(admin.ModelAdmin):  # type: ignore
    """Customize Group model for admin area."""

    list_display: List[str] = [
        "name",
    ]
    list_filter: List[str] = [
        "name",
    ]
    search_fields: List[str] = [
        "name",
    ]
    inlines: Sequence[Type[CommandInline]] = [
        CommandInline,
    ]
