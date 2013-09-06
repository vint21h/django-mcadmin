# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin.py

from django.contrib import admin

from mcadmin.models import ManagementCommandAdminCommand, ManagementCommandAdminGroup

__all__ = ['ManagementCommandAdminGroupAdmin', 'ManagementCommandAdminCommandAdmin', ]


class ManagementCommandAdminCommandAdmin(admin.ModelAdmin):
    """
    Customize ManagementCommandAdminCommand model for admin area.
    """

    list_display = ('command', 'group', )
    list_filter = ('group', )
    search_fields = ('command', 'group__name', )


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

    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )
    inlines = (ManagementCommandAdminCommandInline, )


admin.site.register(ManagementCommandAdminCommand, ManagementCommandAdminCommandAdmin)
admin.site.register(ManagementCommandAdminGroup, ManagementCommandAdminGroupAdmin)
