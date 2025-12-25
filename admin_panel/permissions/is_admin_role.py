from rest_framework import permissions

class IsSuperAdminOrStaff(permissions.BasePermission):
    """
    Allow access only to superusers or users marked as staff (or those with Role.superadmin).
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        # If Role table is present, allow superadmin role
        try:
            if hasattr(user, "admin_role") and user.admin_role.role == "superadmin":
                return True
        except Exception:
            pass
        return False
