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


class ManagementCommandAdminGroupAdmin(admin.ModelAdmin):
    """
    Customize ManagementCommandAdminGroup model for admin area.
    """

    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(ManagementCommandAdminCommand, ManagementCommandAdminCommandAdmin)
admin.site.register(ManagementCommandAdminGroup, ManagementCommandAdminGroupAdmin)
