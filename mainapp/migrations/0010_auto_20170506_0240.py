# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20170506_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='document',
            name='document_path',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='document',
            name='user_selected_document_type',
            field=models.CharField(default='Undefined', max_length=20),
        ),
        migrations.AlterField(
            model_name='document',
            name='type_of_document',
            field=models.CharField(choices=[('BankStatement', 'Account Statement'), ('BankTransfer', 'Bank Transfer'), ('W2', 'Wage and Tax Statement'), ('Undefined', 'Undefined')], default='Undefined', max_length=20),
        ),
        migrations.AlterField(
            model_name='error',
            name='type_of_error',
            field=models.CharField(choices=[('corrupted', 'File Cannot Be Opened'), ('clean', 'No Errors detected'), ('encrypted', 'File Password Protected')], default='clean', max_length=30),
        ),
    ]