# Generated by Django 3.1.2 on 2020-11-06 01:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorter', '0010_auto_20201106_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 4, 23, 45, 671644)),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='method',
            field=models.CharField(max_length=8, verbose_name='Метод'),
        ),
    ]