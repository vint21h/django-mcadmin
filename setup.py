#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django-mcadmin
# setup.py

from setuptools import setup, find_packages

# metadata
VERSION = (0, 2, 0)
__version__ = '.'.join(map(str, VERSION))


setup(
    name="django-mcadmin",
    version=__version__,
    packages=find_packages(),
    install_requires=['Django', 'six', ],
    author="Alexei Andrushievich",
    author_email="vint21h@vint21h.pp.ua",
    description="Easily run django management commands from admin",
    license="GPLv3 or later",
    url="https://github.com/vint21h/django-mcadmin",
    download_url="https://github.com/vint21h/django-mcadmin/archive/%s.tar.gz" % __version__,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Environment :: Plugins",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ]
)
