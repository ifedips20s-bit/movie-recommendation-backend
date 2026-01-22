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
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.movie1 = Movie.objects.create(title="Movie 1")
        self.movie2 = Movie.objects.create(title="Movie 2")

        FavoriteMovie.objects.create(user=self.user, movie=self.movie1)

    def test_trending_movies_endpoint(self):
        url = reverse("trending-movies")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
