from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class TodoAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="api@test.com",
            password="pass123"
        )
        self.client.login(email="api@test.com", password="pass123")

    def test_create_todo(self):
        url = reverse("api-todo-list-create")
        data = {
            "title": "API Todo",
            "status": "pending"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 1)


    def test_list_todos(self):
        Todo.objects.create(user=self.user, title="Todo 1")

        url = reverse("api-todo-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
