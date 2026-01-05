from django.test import TestCase
from django.contrib.auth import get_user_model
from todo.services.todo_service import (
    create_todo,
    update_todo_status,
    delete_todo
)

User = get_user_model()

class TodoServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="service_test",
            email="service@test.com",
            password="pass123"
        )

    def test_create_todo(self):
        todo = create_todo(
            user=self.user,
            title="Service Todo",
            description="Testing service"
        )
        self.assertEqual(todo.title, "Service Todo")
        self.assertEqual(todo.user, self.user)


    def test_update_todo_status(self):
        todo = create_todo(user=self.user, title="Status Todo")
        updated = update_todo_status(todo=todo, status="complete")
        self.assertEqual(updated.status, "complete")


    def test_delete_todo(self):
        todo = create_todo(user=self.user, title="Delete Todo")
        delete_todo(todo=todo)
        self.assertEqual(
            todo.__class__.objects.count(),
            0
        )
