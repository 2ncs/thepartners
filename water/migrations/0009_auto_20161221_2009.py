# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-21 20:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0008_myappuser_price_paroxhs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myappuser',
            old_name='price_paroxhs',
            new_name='price_metapolishs',
        ),
    ]
