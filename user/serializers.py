from django.contrib import auth
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = auth.get_user_model()
        fields = ('id', 'username', 'following')

    def get_following(self, user):
        return user.followers.filter(follower=self.context['request'].user).exists()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
