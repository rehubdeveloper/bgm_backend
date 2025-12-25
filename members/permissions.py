from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods for anyone authenticated (or anonymous if you want),
    but write methods require staff/superuser.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # allow GET, HEAD, OPTIONS for any (or require auth if preferred)
            return True
        # write operations require staff
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
