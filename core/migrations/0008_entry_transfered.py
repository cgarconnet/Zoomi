# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151130_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='transfered',
            field=models.IntegerField(default=0),
        ),
    ]
