# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_run_result_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='result_file',
            field=models.FileField(default='', upload_to=b'media/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
