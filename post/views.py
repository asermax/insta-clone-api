from django.db.models import aggregates
from rest_framework import viewsets, mixins
from insta_clone_api import permissions
from . import models, serializers, filters


class PostViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    queryset = models.Post.objects.annotate(
        likes_count=aggregates.Count('likes', distinct=True),
        comments_count=aggregates.Count('comments', distinct=True),
    )
    serializer_class = serializers.PostSerializer
    filterset_class = filters.PostFilterSet
    permission_classes = (permissions.AuthenticatedCreation,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and self.request.query_params.get('username', '').strip() == '':
            queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filterset_class = filters.CommentFilterSet
    permission_classes = (permissions.AuthenticatedCreation,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and self.request.query_params.get('post', '').strip() == '':
            queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = models.Like.objects.all()
    serializer_class = serializers.LikeSerializer
    filterset_class = filters.LikeFilterSet
    permission_classes = (permissions.AuthenticatedCreation, permissions.AuthorDeletion)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and self.request.query_params.get('post', '').strip() == '':
            queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
