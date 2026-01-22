from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache  # Django cache framework (Redis)
from movies.models import Movie, FavoriteMovie
from movies.serializers import (
    MovieSerializer,
    FavoriteMovieSerializer,
    RecommendedMovieSerializer,
)
from movies.services import get_recommended_movies_for_user


# TTL for Redis cache (seconds)
TRENDING_MOVIES_CACHE_TTL = 60 * 5  # 5 minutes


class TrendingMoviesView(APIView):
    """
    Returns top 10 trending movies based on number of times favorited by users.
    Uses Redis caching for optimization.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Try to get cached trending movies
        cached_data = cache.get('trending_movies')
        if cached_data:
            return Response(cached_data)

        # Query database if cache is empty
        trending_movies = Movie.objects.annotate(
            num_favorites=Count('favorited_by')
        ).order_by('-num_favorites')[:10]

        serializer = MovieSerializer(trending_movies, many=True)
        # Cache the result
        cache.set('trending_movies', serializer.data, TRENDING_MOVIES_CACHE_TTL)

        return Response(serializer.data)


class FavoriteMoviesView(APIView):
    """
    CRUD for user's favorite movies.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Optional: Clear trending cache since favorites changed
            cache.delete('trending_movies')
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RecommendedMoviesView(APIView):
    """
    Returns recommended movies for a user.
    Supports optional filtering, sorting, and pagination.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendations = get_recommended_movies_for_user(request.user)

        # Filter by genre
        genre = request.query_params.get('genre')
        if genre:
            recommendations = [
                movie for movie in recommendations
                if str(movie.get('genre_ids', [])).find(genre) != -1
            ]

        # Sort by popularity or release date
        sort_by = request.query_params.get('sort_by')
        if sort_by in ['popularity', 'release_date']:
            recommendations.sort(key=lambda x: x.get(sort_by, ''), reverse=True)

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        paginated_data = recommendations[start:end]

        serializer = RecommendedMovieSerializer(paginated_data, many=True)
        return Response({
            "page": page,
            "page_size": page_size,
            "total": len(recommendations),
            "results": serializer.data
        })
