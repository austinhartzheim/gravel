# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problems', '0003_auto_20150603_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='last_update_user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='+', default=None),
        ),
    ]
