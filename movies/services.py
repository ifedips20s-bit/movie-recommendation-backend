import requests
from django.conf import settings
from django.core.cache import cache

TMDB_API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"

def get_trending_movies():
    cache_key = "trending_movies"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"{BASE_URL}/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('results', [])
        cache.set(cache_key, data, timeout=60*60)  # cache for 1 hour
        return data
    return []

def get_movie_details(movie_id):
    cache_key = f"movie_{movie_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cache.set(cache_key, data, timeout=60*60)
        return data
    return {}
