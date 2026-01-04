from todo.models import Todo

def get_user_todos(*, user, search=None, status=None):
    """Return Filtered Todo for a user"""
    qs = Todo.objects.filter(user=user)

    if search:
        qs = qs.filter(title__icontains=search)

    if status:
        qs = qs.filter(status = status)

    return qs.order_by("-created_at")