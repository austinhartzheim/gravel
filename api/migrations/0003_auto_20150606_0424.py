# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150605_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedsecret',
            name='shared_secret',
            field=models.BinaryField(max_length=64),
        ),
    ]
