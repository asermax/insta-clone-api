from rest_framework import serializers
from . import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ('id', 'file', 'description')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ('id', 'text', 'create_date', 'user', 'images')
