from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Allows read‐only access for any request,
    but write access only to admin (is_staff) users.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
