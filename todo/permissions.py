from rest_framework.permissions import BasePermission


class IsAdminOrOwnerExceptDelete(BasePermission):
    """
    - Admin can do everything
    - Users can read/update their own objects
    - Only admin can delete
    """

    def has_object_permission(self, request, view, obj):
        
        # Admin Override
        if request.user.is_staff:
            return True
        
        # DELETE - admin only
        if request.method == "DELETE":
            return False
        
        # READ/UPDATE - owner only
        return obj.user == request.user
    
class IsAdminUserStrict(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)