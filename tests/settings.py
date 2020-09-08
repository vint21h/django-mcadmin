# -*- coding: utf-8 -*-

# django-mcadmin
# tests/settings.py


import sys
import random
import pathlib
import tempfile
from typing import Dict, List, Union  # pylint: disable=W0611


# black magic to use imports from library code
sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent.parent.parent))

# secret key
SECRET_KEY = "".join(
    [
        random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")  # nosec
        for i in range(50)
    ]
)  # type: str

# configure databases
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}  # type: Dict[str, Dict[str, str]]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]  # type: List[str]

# configure templates
TEMPLATES = [
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
]  # type: List[Dict[str, Union[str, List[str], bool, Dict[str, Union[str, List[str]]]]]]  # noqa: E501


# add testing related apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django_nose",
    "mcadmin",
]  # type: List[str]

# add nose test runner
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"  # type: str

# configure nose test runner
NOSE_ARGS = [
    "--rednose",
    "--force-color",
    "--with-timer",
    "--with-doctest",
    "--with-coverage",
    "--cover-inclusive",
    "--cover-erase",
    "--cover-package=mcadmin",
    "--logging-clear-handlers",
]  # type: List[str]

# configure urls
ROOT_URLCONF = "mcadmin.urls"  # type: str

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
