# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/migrations/0001_initial.py

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManagementCommandAdminCommand",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("command", models.CharField(help_text="this list get from settings", max_length=255, verbose_name="management command name", db_index=True)),
            ],
            options={
                "ordering": ["command"],
                "verbose_name": "management command",
                "verbose_name_plural": "management commands",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ManagementCommandAdminGroup",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=255, verbose_name="management commands group title", db_index=True)),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "management commands group",
                "verbose_name_plural": "management commands groups",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ManagementCommandAdminGroupPermission",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("group", models.ForeignKey(related_name="permissions", verbose_name="group", to="mcadmin.ManagementCommandAdminGroup")),
                ("user_group", models.ForeignKey(verbose_name="user group", to="auth.Group")),
            ],
            options={
                "ordering": ["group"],
                "verbose_name": "management command group permission",
                "verbose_name_plural": "management command group permissions",
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="managementcommandadmingrouppermission",
            unique_together=set([("group", "user_group")]),
        ),
        migrations.AddField(
            model_name="managementcommandadmincommand",
            name="group",
            field=models.ForeignKey(related_name="commands", verbose_name="group", to="mcadmin.ManagementCommandAdminGroup"),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="managementcommandadmincommand",
            unique_together=set([("command", "group")]),
        ),
    ]
