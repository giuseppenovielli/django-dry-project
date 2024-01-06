from rest_framework import permissions

class Car_user_Write_Permission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            return request.user.groups.filter(name='CarUserWrite').exists()