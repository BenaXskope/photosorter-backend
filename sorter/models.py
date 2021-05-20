from django.db import models as models
from django.db.models import *
from datetime import datetime
import binascii
import os
import uuid


class DirectoryGraph(models.Model):
    abs_path = TextField(verbose_name="Абсолютный путь до папки", blank=True)
    dir_name = TextField(verbose_name="Название папки")
    nodes = IntegerField(verbose_name="Кол-во вершин", default=0)
    edges = IntegerField(verbose_name="Кол-во рёбер", default=0)
    full_edges = IntegerField(verbose_name="Рёбер в полном графе", default=0)

    class Meta:
        verbose_name = "Информация о графе"


class ImageNode(models.Model):
    image = TextField(verbose_name="Изображение", default="")
    real_name = TextField(verbose_name="Название картинки")
    compares = IntegerField(verbose_name="Кол-во сравнений", default=0)
    sumrate = DecimalField(verbose_name="Суммарный рейт", default=0, max_digits=10, decimal_places=8)
    rate = DecimalField(verbose_name="Рейт", default=0, max_digits=10, decimal_places=8)
    relateto = ManyToManyField('self', verbose_name="Связан с", related_name="relatefrom")
    directory = ForeignKey(DirectoryGraph, verbose_name="Папка", on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ('-rate',)
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class ErrorLog(models.Model):
    request = TextField(verbose_name="Запрос")
    error = TextField(verbose_name="Ошибка")
    method = CharField(verbose_name="Метод", max_length=8)
    date = DateTimeField(default=datetime.now())

    class Meta:
        verbose_name = 'Лог ошибки'
        verbose_name_plural = 'Логи ошибок'
