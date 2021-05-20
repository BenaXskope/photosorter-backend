import os
from os import scandir, path
from django.conf.urls.static import static
from django.conf import settings


# def get_directories():
#     return os.listdir(os.path.join(settings.MEDIA_ROOT))


def get_images(directory):
    return os.listdir(directory)
