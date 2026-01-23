from datetime import date
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from movies.models import Movie, FavoriteMovie

User = get_user_model()


class TrendingMoviesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.movie1 = Movie.objects.create(
            tmdb_id=1,
            title="Movie 1",
            overview="Overview 1",
            release_date=date(2024, 1, 1)
        )
        self.movie2 = Movie.objects.create(
            tmdb_id=2,
            title="Movie 2",
            overview="Overview 2",
            release_date=date(2024, 1, 2)
        )

        FavoriteMovie.objects.create(
            user=self.user,
            movie_id=self.movie1.tmdb_id,
            title=self.movie1.title
        )

    def test_trending_movies_endpoint(self):
        response = self.client.get("/api/movies/trending/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
