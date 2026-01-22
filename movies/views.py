from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_trending_movies
from .models import FavoriteMovie
from .serializers import FavoriteMovieSerializer

class TrendingMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movies = get_trending_movies()
        return Response(movies)

class FavoriteMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteMovie.objects.filter(user=request.user)
        serializer = FavoriteMovieSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RecommendedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch recommendations
        recommendations = get_recommended_movies_for_user(request.user)

        # Filtering by genre (optional query param)
        genre = request.query_params.get('genre')
        if genre:
            recommendations = [
                movie for movie in recommendations
                if str(movie.get('genre_ids', [])).find(genre) != -1
            ]

        # Sorting by popularity or release date
        sort_by = request.query_params.get('sort_by')
        if sort_by in ['popularity', 'release_date']:
            recommendations.sort(key=lambda x: x.get(sort_by, ''), reverse=True)

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        paginated_data = recommendations[start:end]

        # Serialize
        serializer = RecommendedMovieSerializer(paginated_data, many=True)
        return Response({
            "page": page,
            "page_size": page_size,
            "total": len(recommendations),
            "results": serializer.data
        })
