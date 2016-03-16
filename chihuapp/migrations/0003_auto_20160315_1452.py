# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chihuapp', '0002_remove_userprofile_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_Time', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='canteen',
            name='delivery_time',
        ),
        migrations.RemoveField(
            model_name='dish',
            name='pictures',
        ),
        migrations.AddField(
            model_name='dish',
            name='canteen',
            field=models.ForeignKey(default=None, to='chihuapp.Canteen'),
        ),
        migrations.AddField(
            model_name='dish',
            name='picture',
            field=models.FileField(default=None, upload_to=b'./dish_img'),
        ),
        migrations.AddField(
            model_name='timeperiod',
            name='Canteen',
            field=models.ForeignKey(to='chihuapp.Canteen'),
        ),
    ]
