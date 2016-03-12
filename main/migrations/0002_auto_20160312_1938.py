# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='result_file',
            field=models.FileField(upload_to=b'uploads/%Y/%m/%d/'),
        ),
    ]
