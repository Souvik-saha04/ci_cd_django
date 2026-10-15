
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPass123!"
        )
        self.login_url = "/api/login/"
        self.welcome_url = "/api/welcome/"

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "TestPass123!"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "WrongPassword"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_welcome_without_token(self):
        response = self.client.get(self.welcome_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_welcome_with_valid_token(self):
        login_response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "TestPass123!"
            },
            format="json"
        )

        access_token = login_response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(self.welcome_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Welcome testuser"
        )
