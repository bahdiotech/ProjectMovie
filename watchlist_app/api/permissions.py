from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        # admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == "GET" or admin_permission



class IsReviewUserOrReadOnly(permissions.BasePermission):
    """ Permission to make sure specific user has access to their individual reviews"""
    def has_object_permission(self, request, view, obj):
        # Note that SAFE_METHODS means GET
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff
