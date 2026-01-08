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

    def test_soft_delete_marks_fields(self):
        todo = Todo.objects.create(
            user=self.user,
            title="Test Todo",
            status="pending"
        )
        todo.soft_delete(user=self.user)

        self.assertTrue(todo.is_deleted)
        self.assertIsNotNone(todo.deleted_at)
        self.assertEqual(todo.deleted_by, self.user)