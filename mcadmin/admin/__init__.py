# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/__init__.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin

from mcadmin.admin.command import CommandAdmin
from mcadmin.admin.group import GroupAdmin
from mcadmin.admin.permissions.command import CommandPermissionAdmin
from mcadmin.admin.permissions.group import CommandGroupPermissionAdmin
from mcadmin.models.command import Command
from mcadmin.models.group import Group
from mcadmin.models.permissions.command import CommandPermission
from mcadmin.models.permissions.group import CommandGroupPermission


__all__ = [
    "CommandAdmin",
    "GroupAdmin",
    "CommandGroupPermissionAdmin",
    "CommandPermissionAdmin",
]  # type: List[str]


# registering admin custom classes
admin.site.register(Command, CommandAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CommandPermission, CommandPermissionAdmin)
admin.site.register(CommandGroupPermission, CommandGroupPermissionAdmin)
