from rest_framework.permissions import BasePermission
class IsJobAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if request.user.is_authenticated and obj.user == request.user.profile else False