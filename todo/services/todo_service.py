def toggle_todo_status(todo):
    """Toggle todo status between pending and complete"""
    todo.status = "complete" if todo.status == "pending" else "pending"
    todo.save(update_fields=["status"])