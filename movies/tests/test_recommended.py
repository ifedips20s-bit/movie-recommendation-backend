from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser


class RecommendedMoviesTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="password123"
        )

        self.client.force_authenticate(user=self.user)
        self.url = reverse("recommended-movies")

    def test_recommended_movies_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
