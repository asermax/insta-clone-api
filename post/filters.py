import django_filters
from . import models


class PostFilterSet(django_filters.FilterSet):
    username = django_filters.CharFilter('user__username')
    feed = django_filters.BooleanFilter(method='filter_user_feed')

    class Meta:
        model = models.Post
        fields = ('username', 'feed')

    def filter_user_feed(self, queryset, name, value):
        if value:
            queryset = queryset.filter(user__followers__follower=self.request.user)

        return queryset


class CommentFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Comment
        fields = ('post',)


class LikeFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Like
        fields = ('post', 'user')
