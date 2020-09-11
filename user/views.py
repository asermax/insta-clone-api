from django.contrib import auth
from rest_framework import viewsets, response, status, exceptions, decorators
from . import serializers


class InvalidCredentialsException(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Las credenciales provistas son inválidas'
    default_code = 'invalid_credentials'


class UserViewSet(viewsets.GenericViewSet):
    queryset = auth.get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    login_serializer_class = serializers.LoginSerializer

    def get_serializer_class(self, login=False):
        if login:
            return self.login_serializer_class
        else:
            return self.serializer_class

    def get_serializer(self, login=False, *args, **kwargs):
        serializer_class = self.get_serializer_class(login)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @decorators.action(detail=False, methods=['post'])
    def login(self, request):
        login_serializer = self.get_serializer(login=True, data=request.data)

        login_serializer.is_valid(raise_exception=True)
        data = login_serializer.validated_data
        user = auth.authenticate(request, username=data['username'], password=data['password'])

        if user is not None:
            auth.login(request, user)
        else:
            raise InvalidCredentialsException()

        serializer = self.get_serializer(instance=user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
