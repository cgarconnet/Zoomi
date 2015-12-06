# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151128_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='assignees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='assignees'),
        ),
    ]
