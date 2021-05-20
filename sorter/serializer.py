from . import models
from rest_framework import serializers
from django.utils import timezone


class DirectoryGraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DirectoryGraph
        fields = (
            'id',
            'dir_name',
            'nodes',
            'edges',
            'full_edges'
        )


class ImageNodeSerializer(serializers.ModelSerializer):

    # image = serializers.ImageField(
    #     max_length=None, use_url=True
    # )

    class Meta:
        model = models.ImageNode
        fields = (
            'id',
            'image',
        )
