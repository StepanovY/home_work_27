from rest_framework import permissions

from selection.models import Selection
from users.models import User


class SelectionUpdatePermission(permissions.BasePermission):
    message = 'Редактировать можно только свою подборку'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
