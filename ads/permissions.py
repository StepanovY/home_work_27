from rest_framework import permissions

from selection.models import Selection
from users.models import User, UserRoles


class AdUpdatePermission(permissions.BasePermission):
    message = 'Редактировать можно только свое объявление'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == UserRoles.MODERATOR or request.user.role == UserRoles.ADMIN:
            return True

        return obj.author == request.user
