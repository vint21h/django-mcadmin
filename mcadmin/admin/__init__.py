# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/admin/__init__.py


from typing import List  # pylint: disable=W0611

from django.contrib import admin

from mcadmin.admin.command import CommandAdmin
from mcadmin.admin.group import GroupAdmin
from mcadmin.admin.permission import GroupPermissionAdmin
from mcadmin.models.command import Command
from mcadmin.models.group import Group
from mcadmin.models.permission import GroupPermission


__all__ = [
    "CommandAdmin",
    "GroupAdmin",
    "GroupPermissionAdmin",
]  # type: List[str]


# registering admin custom classes
admin.site.register(Command, CommandAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupPermission, GroupPermissionAdmin)
