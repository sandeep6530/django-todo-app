from django.urls import path

from .views import (
    TodoListCreateAPIView,
    TodoDetailAPIView,
    LoginAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path("todos/", TodoListCreateAPIView.as_view(), name="api-todo-list-create"),
    path("todos/<int:pk>/", TodoDetailAPIView.as_view(), name="api-todo-detail"),
    path("auth/login/", LoginAPIView.as_view(), name="api-login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="api-logout"),
]
