.. django-mcadmin
.. README.rst

A django-mcadmin documentation
==============================

    *django-mcadmin is a django reusable app that provide simple run management commands from admin*

.. contents::

Warning
------------
* This is a deep BETA and not contain documentation

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://github.com/vint21h/django-mcadmin.git``. Or download latest release from https://github.com/vint21h/django-mcadmin/tags.
* Run ``python ./setup.py install`` from repository source tree or unpacked archive. Or use pip: ``pip install django-mcadmin``.

Configuration
-------------
Add ``"mcadmin"`` to ``settings.INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS += [
        "mcadmin",
    ]

And to ``urls.py``.

.. code-block:: python

    urlpatterns = patterns("",
        url(r"^admin/mcadmin/", include("mcadmin.urls")),
    )


upper of django admin urls.

Licensing
---------
django-mcadmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.

Contacts
--------
**Project Website**: https://github.com/vint21h/django-mcadmin

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.
