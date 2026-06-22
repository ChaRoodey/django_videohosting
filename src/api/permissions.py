from rest_framework.permissions import BasePermission


class IsOwnerOrPublishedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_published:
            return True

        return obj.owner == request.user
