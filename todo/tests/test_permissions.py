from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class PermissionTestAPI(APITestCase):
    def test_admin_can_access_any_todo(self):
        admin = User.objects.create_user(
            username = "admin",
            email = "admin@test.com",
            password = "admin123",
            is_staff = True
        )
        
        myuser = User.objects.create_user(
            username = "user",
            email = "user@test.com",
            password = "user123"
        )

        todo = Todo.objects.create(
            user = myuser,
            title = "User Todo"
        )

        self.client.force_authenticate(user = admin)

        url = reverse(
            "api-todo-detail",
            kwargs = { "version": "v1", "pk": todo.id }
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_delete_todo(self):
        user = User.objects.create_user(
            username = "user",
            email = "user@test.com",
            password = "user123",
        )

        todo = Todo.objects.create(
            user = user,
            title = "User Todo2"
        )

        self.client.force_authenticate(user= user) 

        url = reverse(
            "api-todo-detail",
            kwargs = { "version": "v1", "pk": todo.id }
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    
    def test_admin_can_delete_any_todo(self):
        admin = User.objects.create_user(
            username = "admin",
            email = "admin@test.com",
            password = "admin123",
            is_staff = True
        )

        user = User.objects.create_user(
            username = "user",
            email = "user@test.com",
            password = "user123",
        )

        todo = Todo.objects.create(
            user = user,
            title = "User Todo2"
        )

        self.client.force_authenticate(user = admin)

        url = reverse(
            "api-todo-detail",
            kwargs = { "version": "v1", "pk": todo.id }
        )

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)