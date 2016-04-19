# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chihuapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpermission',
            options={'permissions': (('customer', 'can use customer version'), ('provider', 'can use provider version'))},
        ),
    ]
