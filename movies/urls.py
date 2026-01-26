from django.urls import path
from .views import (
    TrendingMoviesView,
    FavoriteMoviesView,
    RecommendedMoviesView,
    MoviesRootView,
)

urlpatterns = [
    path("", MoviesRootView.as_view(), name="movies-root"),  # root path
    path("trending/", TrendingMoviesView.as_view(), name="trending-movies"),
    path("favorites/", FavoriteMoviesView.as_view(), name="favorite-movies"),
    path("recommended/", RecommendedMoviesView.as_view(), name="recommended-movies"),
]
