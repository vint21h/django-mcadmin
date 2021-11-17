# -*- coding: utf-8 -*-

# django-mcadmin
# tests/settings.py


import sys
import pathlib
import tempfile
from random import SystemRandom
from typing import Any, Dict, List


# black magic to use imports from library code
path = pathlib.Path(__file__).absolute()
project = path.parent.parent.parent
sys.path.insert(0, str(project))

# secret key
SECRET_KEY: str = "".join(
    [
        SystemRandom().choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
        for i in range(50)
    ]
)

# configure databases
DATABASES: Dict[str, Dict[str, str]] = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

MIDDLEWARE: List[str] = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# configure templates
TEMPLATES: List[Dict[str, Any]] = [  # noqa: E501
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]


# add testing related apps
INSTALLED_APPS: List[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "mcadmin",
]

# configure urls
ROOT_URLCONF: str = "mcadmin.urls"

# media/static settings
MEDIA_ROOT = tempfile.gettempdir()
STATIC_ROOT = tempfile.gettempdir()

# locale settings
LANGUAGE_CODE = "en"

# mcadmin settings
MCADMIN_EXAMPLES_PATH = str(pathlib.Path(STATIC_ROOT).joinpath("examples"))
MCADMIN_UPLOADS_PATH = str(pathlib.Path(MEDIA_ROOT).joinpath("uploads"))
MCADMIN_MODULE_NAME = "mcommands"
MCADMIN_USE_PERMISSIONS = False
