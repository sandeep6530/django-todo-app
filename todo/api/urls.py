from django.urls import path

from .views import (
    TodoListCreateAPIView,
    TodoDetailAPIView,
    LoginAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("logout/", LogoutAPIView.as_view(), name="api-logout"),
    path("todos/", TodoListCreateAPIView.as_view(), name="api-todo-list-create"),
    path("todos/<int:pk>/", TodoDetailAPIView.as_view(), name="api-todo-detail"),
]
