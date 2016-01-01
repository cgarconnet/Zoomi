# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 22:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('source', models.IntegerField(blank=True, choices=[(0, 'Manual'), (1, 'Action'), (1, 'Log')], null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]