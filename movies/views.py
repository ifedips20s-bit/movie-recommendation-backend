from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.cache import cache

from movies.models import Movie, FavoriteMovie
from movies.serializers import (
    MovieSerializer,
    FavoriteMovieSerializer,
    RecommendedMovieSerializer,
)
from movies.services import get_recommended_movies_for_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


TRENDING_MOVIES_CACHE_TTL = 60 * 5  # 5 minutes

# ----------------------
# Movies Root View
# ----------------------
class MoviesRootView(APIView):
    """
    Public root endpoint for Movies API.
    Lists all available movie-related endpoints.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Movies API Root",
        operation_description="List of available movie endpoints",
        responses={200: openapi.Response(
            description="Root endpoints",
            examples={
                "application/json": {
                    "message": "Welcome to the Movies API",
                    "endpoints": {
                        "trending": "/api/movies/trending/",
                        "favorites": "/api/movies/favorites/ (JWT required)",
                        "recommended": "/api/movies/recommended/ (JWT required)"
                    }
                }
            }
        )}
    )
    def get(self, request):
        return Response({
            "message": "Welcome to the Movies API",
            "endpoints": {
                "trending": "/api/movies/trending/",
                "favorites": "/api/movies/favorites/ (JWT required)",
                "recommended": "/api/movies/recommended/ (JWT required)"
            }
        })

# ----------------------
# Trending Movies
# ----------------------
class TrendingMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached_data = cache.get("trending_movies")
        if cached_data:
            return Response(cached_data)

        favorite_counts = (
            FavoriteMovie.objects
            .values("movie_id")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        movie_ids = [item["movie_id"] for item in favorite_counts]
        trending_movies = Movie.objects.filter(tmdb_id__in=movie_ids)
        serializer = MovieSerializer(trending_movies, many=True)
        cache.set("trending_movies", serializer.data, TRENDING_MOVIES_CACHE_TTL)

        return Response(serializer.data)


# ----------------------
# Favorite Movies
# ----------------------
class FavoriteMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        FavoriteMovie.objects.create(
            user=request.user,
            movie_id=request.data["movie_id"],
            title=request.data["title"],
            overview=request.data.get("overview", ""),
            poster_path=request.data.get("poster_path", ""),
        )
        cache.delete("trending_movies")
        return Response(status=201)


# ----------------------
# Recommended Movies
# ----------------------
class RecommendedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendations = get_recommended_movies_for_user(request.user)

        genre = request.query_params.get("genre")
        if genre:
            recommendations = [
                movie for movie in recommendations
                if genre in str(movie.get("genre_ids", []))
            ]

        sort_by = request.query_params.get("sort_by")
        if sort_by in ["popularity", "release_date"]:
            recommendations.sort(
                key=lambda x: x.get(sort_by, ""), reverse=True
            )

        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        start = (page - 1) * page_size
        end = start + page_size

        serializer = RecommendedMovieSerializer(
            recommendations[start:end], many=True
        )

        return Response({
            "page": page,
            "page_size": page_size,
            "total": len(recommendations),
            "results": serializer.data,
        })
