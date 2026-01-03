from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("todo/add/", views.addTodo, name="addTodo"),
    path("todo/<int:pk>/edit", views.editTodo, name="editTodo"),
    path("todo/<int:pk>/delete", views.deleteTodo, name="deleteTodo"),
    path("<int:pk>/toggle-status", views.toggleStatus, name="toggleStatus"),
]
