from rest_framework import permissions


class AuthenticatedCreation(permissions.BasePermission):
    message = 'Creation is only available to authed users'

    def has_permisison(self, request, view):
        return view.action != 'create' or request.user.is_authenticated


class AuthorDeletion(permissions.BasePermission):
    message = 'Deletion is only available to author users'
    DEFAULT_AUTHOR_PROP = 'user'

    def has_permisison(self, request, view):
        return view.action != 'delete' or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        author_prop = getattr(view, 'author_prop', self.DEFAULT_AUTHOR_PROP)
        return getattr(obj, author_prop) == request.user
