# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin.py

from __future__ import unicode_literals

from django.contrib import admin

from mcadmin.models import ManagementCommandAdminCommand, ManagementCommandAdminGroup, ManagementCommandAdminGroupPermission

__all__ = [
    "ManagementCommandAdminGroupAdmin",
    "ManagementCommandAdminCommandAdmin",
]


class ManagementCommandAdminCommandAdmin(admin.ModelAdmin):
    """
    Customize ManagementCommandAdminCommand model for admin area.
    """

    list_display = ("command", "group", )
    list_filter = ("group", )
    search_fields = ("command", "group__name", )


class ManagementCommandAdminCommandInline(admin.TabularInline):
    """
    ManagementCommandAdminCommand inline for ManagementCommandAdminGroupAdmin
    """

    model = ManagementCommandAdminCommand
    extra = 1


class ManagementCommandAdminGroupAdmin(admin.ModelAdmin):
    """
    Customize ManagementCommandAdminGroup model for admin area.
    """

    list_display = ("name", )
    list_filter = ("name", )
    search_fields = ("name", )
    inlines = (ManagementCommandAdminCommandInline, )


class ManagementCommandAdminGroupPermissionAdmin(admin.ModelAdmin):
    """
    Customize ManagementCommandAdminGroupPermission model for admin area.
    """

    list_display = ("group", "user_group", )
    list_filter = ("group", "user_group", )
    search_fields = ("group", "user_group__name", )


# registering admin custom classes
admin.site.register(ManagementCommandAdminCommand, ManagementCommandAdminCommandAdmin)
admin.site.register(ManagementCommandAdminGroup, ManagementCommandAdminGroupAdmin)
admin.site.register(ManagementCommandAdminGroupPermission, ManagementCommandAdminGroupPermissionAdmin)
