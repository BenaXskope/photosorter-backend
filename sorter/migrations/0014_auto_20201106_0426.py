# Generated by Django 3.1.2 on 2020-11-06 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorter', '0013_auto_20201106_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 4, 26, 17, 862039)),
        ),
    ]
