from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class TodoViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "view_test",
            email = "view@test.com",
            password= "pass123"
        )

        self.other_user = User.objects.create_user(
            username="other_test",
            email = "other@test.com",
            password = "pass123"
        )

        self.todo = Todo.objects.create(
            user = self.user,
            title = "My Todo"
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logged_in(self):
        self.client.login(email="view@test.com", password="pass123")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/dashboard.html")

    def test_dashboard_logged_in(self):
        self.client.login(email="view@test.com", password="pass123")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/dashboard.html")

    def test_edit_todo_owner_only(self):
        self.client.login(email="other@test.com", password="pass123")

        response = self.client.post(
            reverse("editTodo", args=[self.todo.id]),
            {"title": "Hacked"}
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_todo_owner_only(self):
        self.client.login(email="other@test.com", password="pass123")

        response = self.client.post(
            reverse("deleteTodo", args=[self.todo.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_todo_success(self):
        self.client.login(email="view@test.com", password="pass123")

        response = self.client.post(
            reverse("deleteTodo", args=[self.todo.id])
        )

        self.assertEqual(response.status_code, 302)
        todo = Todo.all_objects.get(id=self.todo.id)
        self.assertTrue(todo.is_deleted)
