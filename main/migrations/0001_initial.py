# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.CharField(unique=True, max_length=64)),
                ('website', models.CharField(max_length=64)),
                ('display_name', models.CharField(max_length=128)),
                ('organization', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=400)),
                ('result_file', models.CharField(unique=True, max_length=64)),
                ('run_type', models.CharField(max_length=2, choices=[(b'AU', b'Automatic'), (b'MA', b'Manual')])),
                ('query_type', models.CharField(max_length=2, choices=[(b'TO', b'Title only'), (b'TD', b'Title + description'), (b'DO', b'Description'), (b'AF', b'All'), (b'UF', b'Other')])),
                ('feedback_type', models.CharField(max_length=2, choices=[(b'NF', b'None'), (b'PF', b'Pseudo'), (b'RF', b'Relevance'), (b'OF', b'Other')])),
                ('map', models.DecimalField(max_digits=200, decimal_places=30)),
                ('p10', models.DecimalField(max_digits=200, decimal_places=30)),
                ('p20', models.DecimalField(max_digits=200, decimal_places=30)),
                ('researcher', models.ForeignKey(to='main.Researcher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=64)),
                ('track_url', models.URLField()),
                ('description', models.CharField(max_length=400)),
                ('genre', models.CharField(max_length=2, choices=[(b'NE', b'News'), (b'WE', b'Web'), (b'BL', b'Blog'), (b'ME', b'Medical'), (b'LE', b'Legal')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('track', models.OneToOneField(primary_key=True, serialize=False, to='main.Track')),
                ('title', models.CharField(unique=True, max_length=64)),
                ('task_url', models.URLField()),
                ('description', models.CharField(max_length=400)),
                ('year', models.IntegerField()),
                ('judgement_file', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='run',
            name='task',
            field=models.ForeignKey(to='main.Task'),
            preserve_default=True,
        ),
    ]
