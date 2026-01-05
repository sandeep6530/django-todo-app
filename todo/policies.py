from rest_framework.permissions import BasePermission

class TodoPolicy:
    @staticmethod
    def can_edit(user, todo):
        return todo.user == user
    
    @staticmethod
    def can_delete(user, todo):
        return todo.user == user
    
    @staticmethod
    def can_view(user, todo):
        return todo.user == user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user