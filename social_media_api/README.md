# Social Media API

This project is a Social Media API built with Django and Django REST Framework.

## Setup

1. Clone the repository.
2. Install the dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## User Authentication

-   Register a new user: `POST /accounts/register/`
-   Login: `POST /accounts/login/`
-   View/Update profile: `GET/PUT /accounts/profile/`

## User Model

The custom user model extends `AbstractUser` and includes the following fields:

-   `bio`: A text field for the user's biography.
-   `profile_picture`: An image field for the user's profile picture.
-   `followers`: A many-to-many relationship to other users.
