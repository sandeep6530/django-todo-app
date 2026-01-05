from django.urls import path

from .views import (
    TodoListCreateAPIView,
    TodoDetailAPIView
)

urlpatterns = [
    path("todos/", TodoListCreateAPIView.as_view(), name="api-todo-list-create"),
    path("todos/<int:pk>/", TodoDetailAPIView.as_view(), name="api-todo-detail"),
]
