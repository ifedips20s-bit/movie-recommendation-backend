"""
URL configuration for config project.
"""
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="Backend API for Movie Recommendation App",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

# Simple root view
def root_view(request):
    return HttpResponse("Welcome to the Movie Recommendation API!")

urlpatterns = [
    path('', root_view),  # <-- Add this line
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/movies/', include('movies.urls')),

    # Swagger documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
