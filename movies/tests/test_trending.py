from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from movies.models import Movie, FavoriteMovie


class TrendingMoviesTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="password123"
        )

        self.movie = Movie.objects.create(
            tmdb_id=202,
            title="Trending Movie",
            overview="Trending overview",
            release_date="2024-01-01",
            poster_path="/poster.jpg"
        )

        FavoriteMovie.objects.create(
            user=self.user,
            movie_id=self.movie.tmdb_id,
            title=self.movie.title,
            overview=self.movie.overview,
            poster_path=self.movie.poster_path,
        )

        self.client.force_authenticate(user=self.user)
        self.url = reverse("trending-movies")

    def test_trending_movies_endpoint(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
