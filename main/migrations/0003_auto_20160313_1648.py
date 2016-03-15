# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20160312_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='researcher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
