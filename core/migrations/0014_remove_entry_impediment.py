# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151206_0115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='impediment',
        ),
    ]
