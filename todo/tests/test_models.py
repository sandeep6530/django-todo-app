from django.test import TestCase
from django.contrib.auth import get_user_model
from todo.models import Todo, AuditLog

User = get_user_model()

class TodoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = "test",
            email="test@example.com",
            password="testpass123"
        )

    def test_create_todo(self):
        todo = Todo.objects.create(
            user=self.user,
            title="Test Todo",
            status="pending"
        )

        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.status, "pending")
        self.assertFalse(todo.is_deleted)

    def test_audit_log_created_on_todo_create(self):
        Todo.objects.create(
            user = self.user,
            title = "Signal Test"
        )

        self.assertEqual(AuditLog.objects.count(), 1)