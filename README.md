🎬 Movie Recommendation API

A scalable and well-documented backend API for a Movie Recommendation application, built with Django REST Framework, optimized with Redis caching, and fully documented using Swagger (OpenAPI).

This project mirrors real-world backend development practices, focusing on performance, security, and developer-friendly API documentation.

🚀 Features
🔹 Movie Recommendations

Fetch trending movies based on user favorites

Generate personalized recommendations

Filter recommendations by genre

Sort results by popularity or release date

Paginated responses for scalability

🔹 User Authentication & Preferences

JWT-based authentication

User registration and login

Save and retrieve favorite movies

Secure access to protected endpoints

🔹 Performance Optimization

Redis caching for trending movie data

Cache invalidation on favorite updates

Reduced database load and faster response times

🔹 API Documentation

Interactive Swagger UI

Clear request/response schemas

Easy frontend integration

🛠️ Tech Stack

Backend: Django, Django REST Framework

Database: PostgreSQL

Caching: Redis (Redis Enterprise Cloud – Free Tier)

Authentication: JWT

Documentation: Swagger (drf-yasg)

Deployment: Render

📂 Project Structure
movie-recommendation-backend/
│
├── config/               # Project settings & URLs
├── movies/               # Movie logic (models, views, services)
├── users/                # Authentication & user management
├── staticfiles/          # Collected static files
├── manage.py
└── README.md

🔑 Authentication

This API uses JWT authentication.

Public Endpoints

POST /users/register/

POST /users/login/

POST /users/token/refresh/

GET /api/movies/ (API root)

Protected Endpoints (JWT required)

GET /api/movies/trending/

GET /api/movies/favorites/

POST /api/movies/favorites/

GET /api/movies/recommended/

📖 API Documentation (Swagger)

Swagger UI is available at:

/api/docs/


Example (local):

http://127.0.0.1:8000/api/docs/

⚡ Caching Strategy

Trending movies are cached using Redis for 5 minutes

Cache is automatically cleared when a user adds a favorite movie

Improves response time and reduces database queries

🧪 Running Locally
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver

✅ Project Status

✔️ API fully functional
✔️ Authentication secured
✔️ Redis caching implemented
✔️ Swagger documentation complete
✔️ Ready for production deployment

👤 Author

Ifedolapo Ajayi
Backend Developer