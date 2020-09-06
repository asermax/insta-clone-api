from rest_framework import viewsets
from . import models, serializers, filters


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    filterset_class = filters.PostFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and self.request.query_params.get('username', '').strip() == '':
            queryset = queryset.none()

        return queryset
