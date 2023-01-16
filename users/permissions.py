from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User
import ipdb

class IsAdmOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.user.is_superuser:
            return True
        
        return False

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated

class IsQualifiedToGetUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User) -> bool:
        # ipdb.set_trace()
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.id is user.id:
            return True

        return False

        return super().has_permission(request, view)