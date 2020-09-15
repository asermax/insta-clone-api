from rest_framework import serializers
from drf_extra_fields import fields
from . import models


class ImageSerializer(serializers.ModelSerializer):
    file = fields.Base64ImageField()

    class Meta:
        model = models.Image
        fields = ('id', 'file', 'description')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Post
        fields = ('id', 'text', 'create_date', 'user', 'images')

    def create(self, validated_data):
        images = validated_data.pop('images')
        post = models.Post.objects.create(**validated_data)
        models.Image.objects.bulk_create([models.Image(post=post, **image) for image in images])

        return post


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'comment', 'create_date', 'user', 'post')
        read_only_fields = ('create_date',)
        extra_kwargs = {'post': {'write_only': True}}
