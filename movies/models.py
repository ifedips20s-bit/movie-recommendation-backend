from django.db import models
from users.models import CustomUser

class FavoriteMovie(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    movie_id = models.IntegerField()  # TMDb movie ID
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_id')

    def __str__(self):
        return f"{self.user.email} - {self.title}"

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)  # TMDb unique movie ID
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=255, null=True, blank=True)
