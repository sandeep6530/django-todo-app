from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from todo.models import Todo

User = get_user_model()


class AuthAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="auth_user",
            email="auth@test.com",
            password="pass123"
        )

    def test_login_api(self):
        url = reverse("api-login")
        data = {"email": "auth@test.com", "password": "pass123"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200) 
        self.assertIn("token", response.data)
        self.assertIn("user_id", response.data)


    def test_logout_api(self):
        login_url = reverse("api-login")
        login_response = self.client.post(
            login_url,
            {"email": "auth@test.com", "password": "pass123"},
            format="json"               
        )
        
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("token", login_response.data)
        
        token = login_response.data["token"]
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        
        logout_url = reverse("api-logout")
        response = self.client.post(logout_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Logged out successfully")
        

    def test_user_cannot_access_others_queryset(self):
        other_user = User.objects.create_user(
            username="other_user",
            email="other@test.com",
            password="pass123"
        )

        other_user_todo = Todo.objects.create(
            user = other_user,
            title = "Private Todo" 
        )

        login_response = self.client.post(
            reverse("api-login"), 
            { "email": "auth@test.com", "password": "pass123"}, 
            format = "json"
        )

        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHRIZATION=f"Token {token}")

        response = self.client.get(reverse("api-todo-detail", args=[other_user_todo.id]))

        self.assertEqual(response.status_code, 401)