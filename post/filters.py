import django_filters
from . import models


class PostFilterSet(django_filters.FilterSet):
    username = django_filters.CharFilter('user__username')

    class Meta:
        model = models.Post
        fields = ('username',)


class CommentFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Comment
        fields = ('post',)


class LikeFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Like
        fields = ('post', 'user')
