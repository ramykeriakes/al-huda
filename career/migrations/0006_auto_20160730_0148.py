# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2016-07-30 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0005_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='jobs_applied',
            field=models.ManyToManyField(blank=True, to='career.Job', verbose_name='Jobs he applied on'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_Name',
            field=models.CharField(help_text='Put your first name, Mandatory', max_length=25, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_Name',
            field=models.CharField(help_text='Put your last name, Mandatory', max_length=25, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='middle_Name',
            field=models.CharField(blank=True, help_text='Put your middle name, Optional', max_length=25, verbose_name='Middle Name'),
        ),
    ]