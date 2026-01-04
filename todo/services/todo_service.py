def toggle_todo_status(todo):
    """Toggle todo status between pending and complete"""
    todo.status = "complete" if todo.status == "pending" else "pending"
    todo.save(update_fields=["status"])

def soft_delete_todo(todo):
    todo.is_deleted = True
    todo.save(update_fields=["is_deleted"])