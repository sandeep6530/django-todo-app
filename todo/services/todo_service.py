from todo.models import Todo
from todo.policies import TodoPolicy

def toggle_todo_status(todo):
    """Toggle todo status between pending and complete"""
    todo.status = "complete" if todo.status == "pending" else "pending"
    todo.save(update_fields=["status"])

def soft_delete_todo(todo):
    todo.is_deleted = True
    todo.save(update_fields=["is_deleted"])


def create_todo(user, title, description=""):
    return Todo.objects.create(
        user=user,
        title=title,
        description=description
    )

def update_todo_status(*, todo, status):
    todo.status = status
    todo.save(update_fields=["status"])
    return todo

def delete_todo(*, todo):
    todo.delete()


def update_todo(todo, user, data):
    if not TodoPolicy.can_edit(user, todo):
        raise PermissionError("Not allowed")
    
    for field, value in data.items():
        setattr(todo, field, value)
    
    todo.save()
    return todo