# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_entry_transfered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='impediment',
            field=models.BooleanField(),
        ),
    ]
