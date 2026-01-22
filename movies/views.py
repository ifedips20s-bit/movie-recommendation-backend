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
        recommendations = get_recommended_movies_for_user(request.user)
        serializer = RecommendedMovieSerializer(recommendations, many=True)
        return Response(serializer.data)