from rest_framework import viewsets, mixins
from . import models, serializers, filters, permissions


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    filterset_class = filters.PostFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and self.request.query_params.get('username', '').strip() == '':
            queryset = queryset.none()

        return queryset


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
