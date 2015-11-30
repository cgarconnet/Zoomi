# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151128_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='duedate',
            field=models.DateField(null=True, blank=True),
        ),
    ]
