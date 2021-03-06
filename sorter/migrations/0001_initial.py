# Generated by Django 3.1.2 on 2020-10-20 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GraphInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodes', models.IntegerField(default=0, verbose_name='Кол-во вершин')),
                ('edges', models.IntegerField(default=0, verbose_name='Кол-во рёбер')),
                ('fulledges', models.IntegerField(default=0, verbose_name='Рёбер в полном графе')),
            ],
            options={
                'verbose_name': 'Информация о графе',
            },
        ),
        migrations.CreateModel(
            name='ImageNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(verbose_name='Изображение')),
                ('compares', models.IntegerField(default=0, verbose_name='Кол-во сравнений')),
                ('sumrate', models.DecimalField(decimal_places=8, default=0, max_digits=10, verbose_name='Суммарный рейт')),
                ('rate', models.DecimalField(decimal_places=8, default=0, max_digits=10, verbose_name='Рейт')),
                ('relateto', models.ManyToManyField(related_name='_imagenode_relateto_+', to='sorter.ImageNode', verbose_name='Связан с')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
                'ordering': ('-rate',),
            },
        ),
    ]
