from django.urls import path
from .views import TrendingMoviesView, FavoriteMoviesView

urlpatterns = [
    path('trending/', TrendingMoviesView.as_view(), name='trending_movies'),
    path('favorites/', FavoriteMoviesView.as_view(), name='favorite_movies'),
]
