from rest_framework import generics, permissions

from todo.selectors.todo_selectors import get_user_todos
from todo.models import Todo
from todo.policies import IsOwner
from todo.api.serializers import TodoSerializer



class TodoListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class TodoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Todo.objects.filter(user = self.request.user)    
    