from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import DiarioDigital


class TokenAuthenticationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="strong-pass-123"
        )
        self.token = Token.objects.create(user=self.user)
        self.diario = DiarioDigital.objects.create(
            nombre="Diario Ejemplo", url_principal="https://example.com"
        )

    def test_api_rejects_requests_without_token(self):
        response = self.client.get("/api/diarios/")
        self.assertIn(response.status_code, (401, 403))

    def test_api_allows_access_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get("/api/diarios/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(any(item["nombre"] == self.diario.nombre for item in payload))
