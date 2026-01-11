from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()

class ThrottleAPITest(APITestCase):
    def test_login_rate_limit(self):
        url = reverse("api-login", kwargs = { "version": "v1" })

        for _ in range(6):
            response = self.client.post(
                url, 
                { "email": "wrong@test.com", "password": "wrong123" },
                format = "json"
            )
        self.assertEqual(response.status_code, 429)