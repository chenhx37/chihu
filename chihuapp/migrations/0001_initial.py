# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Canteen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('delivery_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('pictures', models.URLField()),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('score', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DishAndNumberPair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField()),
                ('dish', models.ForeignKey(to='chihuapp.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField(choices=[(0, b'Finished'), (1, b'Unscored'), (2, b'Canceled'), (3, b'Delivering')])),
                ('total_price', models.FloatField()),
                ('dish_list', models.ManyToManyField(to='chihuapp.DishAndNumberPair')),
            ],
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('customer', 'can use customer version'), ('provider', 'can use customer version')),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('netid', models.CharField(max_length=30)),
                ('school', models.PositiveSmallIntegerField(choices=[(0, b'SunYatSanUniversity')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(to='chihuapp.UserProfile'),
        ),
    ]
