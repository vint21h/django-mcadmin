# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/__init__.py


from typing import List

from django.contrib import admin

from mcadmin.models.group import Group
from mcadmin.admin.group import GroupAdmin
from mcadmin.models.command import Command
from mcadmin.admin.command import CommandAdmin
from mcadmin.models.permissions.command import CommandPermission
from mcadmin.models.permissions.group import CommandGroupPermission
from mcadmin.admin.permissions.command import CommandPermissionAdmin
from mcadmin.admin.permissions.group import CommandGroupPermissionAdmin


__all__: List[str] = [
    "CommandAdmin",
    "GroupAdmin",
    "CommandGroupPermissionAdmin",
    "CommandPermissionAdmin",
]


# registering admin custom classes
admin.site.register(Command, CommandAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CommandPermission, CommandPermissionAdmin)
admin.site.register(CommandGroupPermission, CommandGroupPermissionAdmin)
