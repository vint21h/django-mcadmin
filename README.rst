.. django-mcadmin
.. README.rst

A django-mcadmin documentation
==============================

|Travis|_ |Coveralls|_ |Requires|_ |pypi-license|_ |pypi-version|_ |pypi-python-version|_ |pypi-django-version|_ |pypi-format|_ |pypi-wheel|_ |pypi-status|_

    *django-mcadmin is a django reusable app that provide simple run management commands from admin*

.. contents::

Installation
------------
* Obtain your copy of source code from the git repository: ``$ git clone https://github.com/vint21h/django-mcadmin.git``. Or download the latest release from https://github.com/vint21h/django-mcadmin/tags/.
* Run ``$ python ./setup.py install`` from the repository source tree or unpacked archive. Or use pip: ``$ pip install django-mcadmin``.

Configuration
-------------
* Add ``"mcadmin"`` to ``settings.INSTALLED_APPS``:

.. code-block:: python

    # settings.py

    INSTALLED_APPS += [
        "mcadmin",
    ]

* Add ``"mcadmin"`` to your URLs definitions:

.. code-block:: python

    # urls.py

    from django.conf.urls import url


    urlpatterns += [
        url(r"^admin/mcadmin/", include("mcadmin.urls")),
    ]

* Run ``$ python ./manage.py migrate`` in your project folder to apply app migrations.

Settings
--------
``MCADMIN_EXAMPLES_PATH``
    Management commands files templates path. Defaults to: ``settings.STATIC_ROOT``.

``MCADMIN_UPLOADS_PATH``
    Management commands forms with files upload path. Defaults to: ``settings.MEDIA_ROOT``.

``MCADMIN_MODULE_NAME``
    Management commands admin classes search module name. Defaults to: ``"mcommands"``.

``MCADMIN_USE_PERMISSIONS``
    Management commands admin classes search module name. Defaults to: ``False``.

Usage
-----

Licensing
---------
django-mcadmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.

Contacts
--------
**Project Website**: https://github.com/vint21h/django-mcadmin/

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.


.. |Travis| image:: https://travis-ci.org/vint21h/django-mcadmin.svg?branch=master
    :alt: Travis
.. |Coveralls| image:: https://coveralls.io/repos/github/vint21h/django-mcadmin/badge.svg?branch=master
    :alt: Coveralls
.. |Requires| image:: https://requires.io/github/vint21h/django-mcadmin/requirements.svg?branch=master
    :alt: Requires
.. |pypi-license| image:: https://img.shields.io/pypi/l/django-mcadmin
    :alt: License
.. |pypi-version| image:: https://img.shields.io/pypi/v/django-mcadmin
    :alt: Version
.. |pypi-django-version| image:: https://img.shields.io/pypi/djversions/django-mcadmin
    :alt: Supported Django version
.. |pypi-python-version| image:: https://img.shields.io/pypi/pyversions/django-mcadmin
    :alt: Supported Python version
.. |pypi-format| image:: https://img.shields.io/pypi/format/django-mcadmin
    :alt: Package format
.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/django-mcadmin
    :alt: Python wheel support
.. |pypi-status| image:: https://img.shields.io/pypi/status/django-mcadmin
    :alt: Package status
.. _Travis: https://travis-ci.org/vint21h/django-mcadmin/
.. _Coveralls: https://coveralls.io/github/vint21h/django-mcadmin?branch=master
.. _Requires: https://requires.io/github/vint21h/django-mcadmin/requirements/?branch=master
.. _pypi-license: https://pypi.org/project/django-mcadmin/
.. _pypi-version: https://pypi.org/project/django-mcadmin/
.. _pypi-django-version: https://pypi.org/project/django-mcadmin/
.. _pypi-python-version: https://pypi.org/project/django-mcadmin/
.. _pypi-format: https://pypi.org/project/django-mcadmin/
.. _pypi-wheel: https://pypi.org/project/django-mcadmin/
.. _pypi-status: https://pypi.org/project/django-mcadmin/
