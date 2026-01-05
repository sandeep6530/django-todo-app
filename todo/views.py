from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse

from todo.selectors.todo_selectors import get_user_todos
from todo.services.todo_service import toggle_todo_status, soft_delete_todo
from .models import Todo
from .forms import TodoForm


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("search")
        status_filter = request.GET.get("status")
        
        todo_list = get_user_todos(user=request.user, search=search_query, status=status_filter)

        paginator = Paginator(todo_list, 5)
        page_number = request.GET.get("page")
        todos = paginator.get_page(page_number)

        return render(request, "todos/dashboard.html", {"todos": todos})


@login_required
def dashboard(request):
    # todo_list = Todo.objects.filter(user=request.user).select_related("user").order_by("-created_at")
    # paginator = Paginator(todo_list, 10)
    # page_number = request.GET.get("page")
    # todos = paginator.get_page(page_number)

    search_query = request.GET.get("search")
    status_filter = request.GET.get("status")
    
    todo_list = get_user_todos(user=request.user, search=search_query, status=status_filter)

    paginator = Paginator(todo_list, 5)
    page_number = request.GET.get("page")
    todos = paginator.get_page(page_number)

    return render(request, "todos/dashboard.html", {"todos": todos})


class AddTodoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TodoForm()
        return render(request, "todos/addTodo.html", { "form": form })
    
    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST, initial = { "user": request.user })
        if form.is_valid():
            todo = form.save(commit = False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo created successfully!")
            return redirect("dashboard")

@login_required
def addTodo(request):
    if request.method == "POST":
        form = TodoForm(request.POST, initial={ "user": request.user })
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo created successfully!")
            return redirect("dashboard")
    else:
        form = TodoForm()

    return render(request, "todos/addTodo.html", { "form": form })


class EditTodoView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(Todo, id=pk, user = request.user)
        form = TodoForm(instance = todo)
        return render(request, "todos/editTodo.html", {"form": form})
    
    def post(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(Todo, user=request.user, id=pk)
        form = TodoForm(request.POST, instance = todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully!")
            return redirect("dashboard")


@login_required
def editTodo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully!")
            return redirect("dashboard")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todos/editTodo.html", {"form": form})


class DeleteTodoView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(Todo, id=pk, user = request.user)
        soft_delete_todo(todo)
        messages.info(request, f"{todo.title} is deleted.")
        return redirect("dashboard")


@login_required
def deleteTodo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    soft_delete_todo(todo)
    messages.info(request, f"{todo.title} is deleted.")
    return redirect("dashboard")


@login_required
def toggleStatus(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)

    toggle_todo_status(todo)
    return redirect("dashboard")