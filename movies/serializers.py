from rest_framework import serializers
from .models import FavoriteMovie, Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['tmdb_id', 'title', 'overview', 'release_date', 'poster_path']

class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ['id', 'movie_id', 'title', 'overview', 'poster_path']


class RecommendedMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField()
    poster_path = serializers.CharField()
    release_date = serializers.CharField()
    genre_ids = serializers.ListField(child=serializers.IntegerField())
    vote_average = serializers.FloatField()
