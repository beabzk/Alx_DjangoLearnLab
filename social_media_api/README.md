# Social Media API

This project is a Social Media API built with Django and Django REST Framework.

## Live URL

- Render: https://sma-jvqc.onrender.com

## Setup (local)

1. Clone the repository.
2. Install the dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

Base API path: `/api/`

## User Authentication

- Register a new user: `POST /api/accounts/register/`
- Login: `POST /api/accounts/login/`
- View/Update profile: `GET/PUT /api/accounts/profile/`

## Posts & Comments

- Posts: CRUD via DRF router at `/api/posts/`
- Comments: CRUD via DRF router at `/api/comments/`
- Feed: `GET /api/feed/`
- Like a post: `POST /api/posts/<id>/like/`
- Unlike a post: `DELETE /api/posts/<id>/unlike/`
- Notifications: `GET /api/notifications/`

## Quick test with curl

- Register (get token):
  curl -sS -X POST https://sma-jvqc.onrender.com/api/accounts/register/ \
       -H "Content-Type: application/json" \
       -d '{"username":"demo_user","password":"Passw0rd!","email":"demo_user@example.com"}'

- Login (get token):
  curl -sS -X POST https://sma-jvqc.onrender.com/api/accounts/login/ \
       -H "Content-Type: application/json" \
       -d '{"username":"demo_user","password":"Passw0rd!"}'

- Authenticated list posts (replace TOKEN):
  curl -sS https://sma-jvqc.onrender.com/api/posts/ \
       -H "Authorization: Token TOKEN"

## Deploying to Render

- Create a Postgres database on Render and copy its `External Database URL`.
- Create a Web Service from this repo with root set to `social_media_api`.
  - Build Command:
    - `pip install -r requirements.txt`
    - `python manage.py collectstatic --no-input`
  - Start Command:
    - `gunicorn social_media_api.wsgi:application --log-file -`
- Environment Variables:
  - `SECRET_KEY`: strong random string
  - `DJANGO_DEBUG`: `False`
  - `DJANGO_ALLOWED_HOSTS`: `sma-jvqc.onrender.com`
  - `DJANGO_SECURE_SSL_REDIRECT`: `True`
  - `DJANGO_CSRF_TRUSTED_ORIGINS`: `https://sma-jvqc.onrender.com`
  - `DATABASE_URL`: value from Render Postgres
- After first deploy, run (via Render Shell):
  - `python manage.py migrate`
  - Optionally: `python manage.py createsuperuser`

## Notes

- Static files are served by WhiteNoise (`collectstatic` required).
- For media uploads in production, use S3 + django-storages.
- Add CORS if needed for browser clients.
