# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0003_auto_20161212_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='Arrival_Date',
            field=models.CharField(max_length=50, verbose_name='Arraval Date'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Contact_App',
            field=models.CharField(max_length=135, verbose_name='Application'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Discount',
            field=models.CharField(max_length=135, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Email',
            field=models.CharField(max_length=135, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='First_Name',
            field=models.CharField(max_length=135, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Net_Price',
            field=models.CharField(max_length=135, verbose_name='Net Price'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Order_Code',
            field=models.CharField(max_length=135, verbose_name='Order Code'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Order_Date',
            field=models.CharField(max_length=135, verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Payment_Fee',
            field=models.CharField(max_length=135, verbose_name='Payment Fee'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Payment_Status',
            field=models.CharField(max_length=135, verbose_name='Payment Status'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Promo_Code',
            field=models.CharField(blank=True, max_length=135, verbose_name='Promo Code'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Service_Days',
            field=models.CharField(max_length=50, verbose_name='Service Days'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Social_Profile',
            field=models.CharField(max_length=135, verbose_name='Social Profile'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Social_Profile_Name',
            field=models.CharField(max_length=135, verbose_name='Social Profile Name/Number'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Surname',
            field=models.CharField(max_length=135, verbose_name='Surname'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='Total',
            field=models.CharField(max_length=135, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='myappuser',
            name='code',
            field=models.CharField(blank=True, max_length=135, verbose_name='Promo Code'),
        ),
        migrations.AlterField(
            model_name='myappuser',
            name='status',
            field=models.TextField(blank=True, default='Not Used', editable='True', verbose_name='Status'),
        ),
    ]
