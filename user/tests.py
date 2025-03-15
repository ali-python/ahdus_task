from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class UserAuthTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "securepassword",
            "username": "testuser"
        }
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password"],
            username=self.user_data["username"]
        )

    def test_login_invalid_credentials(self):
        response = self.client.post("/auth/login/", {"email": "wrong@example.com", "password": "wrongpass"})
        self.assertEqual(response.status_code, 400)

    def test_login_user_missing_fields(self):
        response = self.client.post("/auth/login/", {"email": ""})
        self.assertEqual(response.status_code, 400)

    def test_login_user_success(self):
        response = self.client.post("/auth/login/", {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        self.assertEqual(response.status_code, 200)

    def test_register_user_missing_fields(self):
        response = self.client.post("/auth/register/", {"email": "new@example.com"})
        self.assertEqual(response.status_code, 400)

    def test_register_user_success(self):
        response = self.client.post("/auth/register/", {
            "email": "new@example.com",
            "password": "securepassword",
            "username": "newuser"
        })
        self.assertEqual(response.status_code, 201)
