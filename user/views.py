from django.contrib import auth
from rest_framework import viewsets, response, status, exceptions, decorators, permissions, mixins
from . import serializers


class InvalidCredentialsException(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Las credenciales provistas son inválidas'
    default_code = 'invalid_credentials'


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = auth.get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    login_serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'

    def get_serializer_class(self, login=False):
        if login:
            return self.login_serializer_class
        else:
            return self.serializer_class

    def get_serializer(self, login=False, *args, **kwargs):
        serializer_class = self.get_serializer_class(login)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @decorators.action(detail=False, methods=('post',), permission_classes=(permissions.AllowAny,))
    def login(self, request):
        login_serializer = self.get_serializer(data=request.data, login=False)

        login_serializer.is_valid(raise_exception=True)
        data = login_serializer.validated_data
        user = auth.authenticate(request, username=data['username'], password=data['password'])

        if user is not None:
            auth.login(request, user)
        else:
            raise InvalidCredentialsException()

        serializer = self.get_serializer(instance=user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=('get',))
    def me(self, request):
        serializer = self.get_serializer(instance=self.request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=True, methods=('post',))
    def follow(self, request, username=None):
        user = self.get_object()
        follow = request.user.following.create(following=user)

        return response.Response(data={'id': follow.id}, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=('delete',))
    def unfollow(self, request, username=None):
        request.user.following.filter(following__username=username).delete()

        return response.Response(status=status.HTTP_204_NO_CONTENT)
