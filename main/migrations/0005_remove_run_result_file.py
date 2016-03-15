# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160313_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='run',
            name='result_file',
        ),
    ]
