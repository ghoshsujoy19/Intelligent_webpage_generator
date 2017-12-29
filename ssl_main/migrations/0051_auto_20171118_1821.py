# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssl_main', '0050_auto_20171118_1816'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DepartmentN',
            new_name='Department',
        ),
        migrations.RemoveField(
            model_name='teachingn',
            name='user',
        ),
        migrations.AlterField(
            model_name='projects',
            name='status',
            field=models.CharField(choices=[('ongoing', '0'), ('Completed', '1')], max_length=200),
        ),
        migrations.AlterField(
            model_name='students',
            name='course',
            field=models.CharField(choices=[('Ph.D.', 'Ph.D.'), ('M.Tech', 'M.Tech'), ('B.Tech', 'B.Tech')], max_length=200),
        ),
        migrations.AlterField(
            model_name='students',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Continuing', 'Continuing')], max_length=200),
        ),
        migrations.AlterField(
            model_name='teaching',
            name='semester',
            field=models.CharField(choices=[('Odd Semester', 'Odd Semester'), ('Even Semester', 'Even Semester')], default='Odd Semester', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(choices=[('Design', 'Design'), ('Chemical Engineering', 'Chemical Engineering'), ('Chemistry', 'Chemistry'), ('Mathematics', 'Mathematics'), ('Bio-Tech', 'Bio-Tech'), ('Humanities', 'Humanities'), ('Civil Engineering', 'Civil Engineering'), ('Computer Science and Engineering', 'Computer Science and Engineering'), ('Electronics and Electrical Engineering', 'Electronics and Electrical Engineering'), ('Physics', 'Physics'), ('Mechanical Engineering', 'Mechanical Engineering')], default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='designation',
            field=models.CharField(choices=[('Associate Professor', 'Associate Professor'), ('Assistant Professor', 'Assistant Professor'), ('Head of Department', 'Head of Department'), ('Professor', 'Professor')], default='', max_length=50),
        ),
        migrations.DeleteModel(
            name='TeachingN',
        ),
    ]