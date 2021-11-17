# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/__init__.py


from typing import List

from mcadmin.models.group import Group
from mcadmin.models.command import Command
from mcadmin.models.permissions.command import CommandPermission
from mcadmin.models.permissions.group import CommandGroupPermission


__all__: List[str] = [
    "Command",
    "Group",
    "CommandPermission",
    "CommandGroupPermission",
]
