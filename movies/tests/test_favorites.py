from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from movies.models import FavoriteMovie

User = get_user_model()


class FavoriteMoviesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_add_favorite_movie(self):
        payload = {
            "movie_id": 123,
            "title": "Test Movie",
            "overview": "Some overview",
            "poster_path": "/poster.jpg"
        }

        response = self.client.post(
            "/api/movies/favorites/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteMovie.objects.count(), 1)

    def test_list_favorites(self):
        FavoriteMovie.objects.create(
            user=self.user,
            movie_id=123,
            title="Test Movie"
        )

        response = self.client.get("/api/movies/favorites/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
