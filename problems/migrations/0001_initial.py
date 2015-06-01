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
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
                ('reference', models.TextField()),
                ('description', models.TextField()),
                ('userauthed', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=40, null=True, default=None)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_closed', models.DateTimeField(null=True, default=None)),
                ('resolved', models.BooleanField(default=False)),
                ('percent_complete', models.PositiveSmallIntegerField(default=0)),
                ('assigned_to', models.ManyToManyField(null=True, default=None, to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('text', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='responses',
            field=models.ManyToManyField(to='problems.Reply'),
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='problems.ProblemTag'),
        ),
        migrations.AddField(
            model_name='problem',
            name='userref',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+', default=None, null=True),
        ),
    ]
