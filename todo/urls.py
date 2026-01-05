from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("todo/add/", views.AddTodoView.as_view(), name="addTodo"),
    path("todo/<int:pk>/edit", views.EditTodoView.as_view(), name="editTodo"),
    path("todo/<int:pk>/delete", views.DeleteTodoView.as_view(), name="deleteTodo"),
    path("<int:pk>/toggle-status", views.toggleStatus, name="toggleStatus"),
]
