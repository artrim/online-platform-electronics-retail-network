from rest_framework import permissions


class IsUsers(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False
