# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_entry_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='assignees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='assignees'),
        ),
        migrations.AddField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 11, 27, 12, 18, 54, 570915, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='done',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='entry',
            name='duedate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='impediment',
            field=models.IntegerField(default=0),
        ),
    ]
