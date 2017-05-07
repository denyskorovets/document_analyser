# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctype',
            name='document',
        ),
        migrations.AddField(
            model_name='document',
            name='type_of_document',
            field=models.CharField(choices=[('BankStatement', 'Account Statement'), ('BankTransfer', 'Bank Transfer'), ('W2', 'Wage and Tax Statement'), ('Undefined', 'Undefined')], default='Undefined', max_length=10),
        ),
        migrations.DeleteModel(
            name='DocType',
        ),
    ]
