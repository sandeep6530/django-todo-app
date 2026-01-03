from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Todo


@login_required
def dashboard(request):
    # todo_list = Todo.objects.filter(user=request.user).select_related("user").order_by("-created_at")
    # paginator = Paginator(todo_list, 10)
    # page_number = request.GET.get("page")
    # todos = paginator.get_page(page_number)

    todo_list = Todo.objects.filter(user=request.user)
    search_query = request.GET.get("search")
    status_filter = request.GET.get("status")
    if search_query:
         todo_list = todo_list.filter(title__icontains=search_query)
    
    if status_filter:
         todo_list = todo_list.filter(status=status_filter)

    todo_list = todo_list.select_related("user").order_by("-created_at")
    paginator = Paginator(todo_list, 5)
    page_number = request.GET.get("page")
    todos = paginator.get_page(page_number)

    return render(request, "todos/dashboard.html", { "todos": todos })


@login_required
def addTodo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        descrption = request.POST.get("descrption")
        Todo.objects.create(
            user = request.user,
            title= title,
            descrption = descrption
        )
        messages.success(request, "Todo created successfully!")
        return redirect("dashboard")
    
    return render(request, "todos/addTodo.html")


@login_required
def editTodo(request, pk):
        todo = get_object_or_404(Todo, id=pk, user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("discription")
            status = request.POST.get("status")
            todo.title = title
            todo.description = description
            todo.status = status
            todo.save()
            messages.success(request, "Todo updated successfully!")
            return redirect("dashboad")
        return render(request, "todos/editTodo.html", { "todo": todo })


@login_required
def deleteTodo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        messages.info(request, f"{todo.title} is deleted.")
        return redirect("dashboard")