# Generated by Django 3.1.2 on 2020-11-06 16:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sorter', '0015_auto_20201106_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 19, 52, 15, 822992)),
        ),
        migrations.AlterField(
            model_name='imagenode',
            name='directory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='sorter.directorygraph', verbose_name='Папка'),
        ),
    ]
