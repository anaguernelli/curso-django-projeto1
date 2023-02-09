from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # User que está buscando recipe for o mesmo que está logado
        return obj.author == request.user

    def has_permission(self, request, view):
        return super().has_permission(request, view)
