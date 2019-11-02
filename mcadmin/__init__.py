# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/__init__.py


from typing import List  # pylint: disable=W0611


__all__ = ["default_app_config"]  # type: List[str]


default_app_config = "mcadmin.apps.DjangoManagementCommandsAdminConfig"
