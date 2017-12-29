# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-14 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssl_main', '0023_auto_20171113_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Continuing', 'Continuing')], max_length=200),
        ),
        migrations.AlterField(
            model_name='teaching',
            name='semester',
            field=models.CharField(choices=[('Even Semester', 'Even Semester'), ('Odd Semester', 'Odd Semester')], default='Odd Semester', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='designation',
            field=models.CharField(choices=[('Professor', 'Professor'), ('Assistant Professor', 'Assistant Professor'), ('Associate Professor', 'Associate Professor')], default='', max_length=50),
        ),
    ]