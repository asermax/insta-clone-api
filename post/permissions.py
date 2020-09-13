from rest_framework import permissions


class AuthenticatedCreation(permissions.BasePermission):
    message = 'Creation is only available to authed users'

    def has_permisison(self, request, view):
        return view.action != 'create' or request.user.is_authenticated
