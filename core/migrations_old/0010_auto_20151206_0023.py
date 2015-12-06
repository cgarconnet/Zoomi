# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20151206_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='transfered',
            field=models.BooleanField(),
        ),
    ]
