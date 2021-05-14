.. django-mcadmin
.. README.rst

A django-mcadmin documentation
==============================

|GitHub|_ |Coveralls|_ |pypi-license|_ |pypi-version|_ |pypi-python-version|_ |pypi-django-version|_ |pypi-format|_ |pypi-wheel|_ |pypi-status|_

    *django-mcadmin is a Django reusable app that provides simple run management commands from admin*

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

    from django.urls import re_path, include


    urlpatterns += [
        re_path(r"^admin/mcadmin/", include("mcadmin.urls")),
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
For example, exists management command like this:

.. code-block:: python

    # management/commands/something-useless.py

    from django.core.management.base import BaseCommand


    class Command(BaseCommand):

        help = "Useless management command"

        def add_arguments(self, parser):

            parser.add_argument(
                "--object-id",
                "-o",
                dest="object_id",
                help="Object ID",
                action="store",
                required=True,
                metavar="OBJECT_ID",
                type=int,
            )

        def handle(self, *args, **kwargs):

            self.stdout.write(kwargs.get("object_id"))

Next, you need to create a form for this management command admin which we use in the next piece of code:

.. code-block:: python

    # forms.py

    from django import forms


    class SomethingUselessManagementCommandAdminForm(forms.Form):

        object_id = forms.IntegerField(label="Object ID", required=True)

And finally, write management command admin class and register it:

.. code-block:: python

    # mcommands/something-useless.py

    from mcadmin.command import ManagementCommandAdmin
    from mcadmin.registry import registry

    from forms import SomethingUselessManagementCommandAdminForm


    class SomethingUselessManagementCommandAdmin(ManagementCommandAdmin):

        command = "something-useless"
        name = "Useless management command"
        form = SomethingUselessManagementCommandAdminForm


    # registering management command admin custom classes
    registry.register(command=SomethingUselessManagementCommandAdmin)

Also, there are some helpers for building more complex flows, like management commands that can be executed directly or as a background task or management commands that handle uploaded files. For example:

Management command:

.. code-block:: python

    # management/commands/distributed-something-useless-with-file.py

    from mcadmin.management.commands import TaskCommand


    class Command(TaskCommand):

        help = "Useless management command which process file uploaded from a command from and can be executed directly or as background task"

        def add_arguments(self, parser):

            parser.add_argument(
                "--task",
                "-T",
                dest="as_task",
                help="Run command as background task",
                default=False,
                action="store",
                metavar="TASK",
                type=bool,
            )
            parser.add_argument(
                "--object-id",
                "-o",
                dest="object_id",
                help="Object ID",
                action="store",
                required=True,
                metavar="OBJECT_ID",
                type=int,
            )
            parser.add_argument(
                "--data",
                "-D",
                dest="data",
                help="Path to file with data",
                action="store",
                metavar="DATA",
                type=str,
            )

        def _local(self, *args, **kwargs):

            self.stdout.write(kwargs.get("object_id"))
            self.stdout.write(kwargs.get("data"))

        def _as_task(self, *args, **kwargs):

            # There must be code which executed in threads or call celery task or something else asynchronous.
            self.stdout.write(kwargs.get("object_id"))
            self.stdout.write(kwargs.get("data"))

Management command admin form:

.. code-block:: python

    # forms.py

    from django import forms

    from mcadmin.forms.helpers import (
        ManagementCommandAdminTaskForm,
        ManagementCommandAdminFilesForm
    )


    class DistributedSomethingUselessWithFileManagementCommandAdminForm(
        ManagementCommandAdminTaskForm,
        ManagementCommandAdminFilesForm
    ):

        data = forms.FileField(label="data, required=True)
        object_id = forms.IntegerField(label="Object ID", required=True)

Management command admin example file:

.. code-block:: python

    # mcommands/examples.py

    from mcadmin.example import ManagementCommandAdminExampleFile


    class DistributedSomethingUselessWithFileManagementCommandAdminExampleFile(
        ManagementCommandAdminExampleFile
    ):

        description = "Management command with files example file"
        path = "distributed-something-useless-with-file-example.csv"

Or for the file which not served using Django but directly available for download via HTTP:

.. code-block:: python

    # mcommands/examples.py

    from mcadmin.example import ManagementCommandAdminExampleFile


    class DistributedSomethingUselessWithFileManagementCommandAdminExampleFile(
        ManagementCommandAdminExampleFile
    ):

        description = "Management command with files example file"
        path = "https://www.example.com/distributed-something-useless-with-file-example.csv"
        raw = True

Management command admin:

.. code-block:: python

    # mcommands/something-useless.py

    from mcadmin.command import ManagementCommandAdmin
    from mcadmin.registry import registry

    from forms import DistributedSomethingUselessWithFileManagementCommandAdminForm


    class DistributedSomethingUselessWithFileManagementCommandAdmin(ManagementCommandAdmin):

        command = "distributed-something-useless-with-file"
        name = "Distributed useless management command with file"
        form = DistributedSomethingUselessWithFileManagementCommandAdminForm
        examples = [DistributedSomethingUselessWithFileManagementCommandAdminExampleFile]


    # registering management command admin custom classes
    registry.register(command=DistributedSomethingUselessWithFileManagementCommandAdmin)

Licensing
---------
django-mcadmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.

Contacts
--------
**Project Website**: https://github.com/vint21h/django-mcadmin/

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.


.. |GitHub| image:: https://github.com/vint21h/django-mcadmin/workflows/build/badge.svg
    :alt: GitHub
.. |Coveralls| image:: https://coveralls.io/repos/github/vint21h/django-mcadmin/badge.svg?branch=master
    :alt: Coveralls
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
.. _GitHub: https://github.com/vint21h/django-mcadmin/actions/
.. _Coveralls: https://coveralls.io/github/vint21h/django-mcadmin?branch=master
.. _pypi-license: https://pypi.org/project/django-mcadmin/
.. _pypi-version: https://pypi.org/project/django-mcadmin/
.. _pypi-django-version: https://pypi.org/project/django-mcadmin/
.. _pypi-python-version: https://pypi.org/project/django-mcadmin/
.. _pypi-format: https://pypi.org/project/django-mcadmin/
.. _pypi-wheel: https://pypi.org/project/django-mcadmin/
.. _pypi-status: https://pypi.org/project/django-mcadmin/
