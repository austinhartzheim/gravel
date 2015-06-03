# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20150602_0312'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='last_updated',
            field=models.DateTimeField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='reply',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
