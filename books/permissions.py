from rest_framework.permissions import (
    SAFE_METHODS, BasePermission,
)
from rest_framework.request import Request


class IsAdminOrReadOnly(BasePermission):
    def has_permission(
            self,
            request: Request,
            view: object) -> bool:
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
            )
            or (request.user and request.user.is_staff)
        )
