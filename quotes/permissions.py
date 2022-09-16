from rest_framework.permissions import BasePermission

class QuotePermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        else:
            return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return obj.user == request.user or request.user.is_superuser
        else:
            return True

class ContentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        else:
            return request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        else:
            return True