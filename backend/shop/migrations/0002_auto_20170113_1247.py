# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 11:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Narocilo',
            new_name='Order',
        ),
    ]
