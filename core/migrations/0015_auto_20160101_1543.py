# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-01 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='completed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Theme'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
