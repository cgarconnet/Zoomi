# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151127_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='assignees',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, related_name='assignees'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='order',
            field=models.IntegerField(default=1000),
        ),
    ]
