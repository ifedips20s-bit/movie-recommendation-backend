from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class RecommendedMoviesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_recommended_movies_endpoint(self):
        response = self.client.get("/api/movies/recommended/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
