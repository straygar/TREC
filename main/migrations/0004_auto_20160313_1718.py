# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160313_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='result_file',
            field=models.FileField(null=True, upload_to=b'media/%Y/%m/%d/', blank=True),
        ),
    ]
