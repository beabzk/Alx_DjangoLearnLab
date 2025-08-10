from django.urls import path
from . import views

"""
URL Configuration for the API app.

This module defines all the URL patterns for the Book and Author API endpoints.
Each view is mapped to a specific URL pattern that follows RESTful conventions.

URL Patterns:
- /books/ - List all books (GET)
- /books/create/ - Create a new book (POST)
- /books/<int:pk>/ - Retrieve a specific book (GET)
- /books/update/<int:pk>/ - Update a specific book (PUT/PATCH)
- /books/delete/<int:pk>/ - Delete a specific book (DELETE)
- /authors/ - List all authors with their books (GET)
- /authors/create/ - Create a new author (POST)
- /authors/<int:pk>/ - Retrieve a specific author with books (GET)
"""

app_name = 'api'

urlpatterns = [
    # Book endpoints - CRUD operations
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),

    # Author endpoints - Read operations and create
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]

"""
URL Pattern Explanation:

Book Endpoints:
- GET /api/books/ - Retrieve all books
- POST /api/books/create/ - Create a new book (requires authentication)
- GET /api/books/{id}/ - Retrieve a specific book by ID
- PUT/PATCH /api/books/update/{id}/ - Update a book (requires authentication)
- DELETE /api/books/delete/{id}/ - Delete a book (requires authentication)

Author Endpoints:
- GET /api/authors/ - Retrieve all authors with their books
- POST /api/authors/create/ - Create a new author (requires authentication)
- GET /api/authors/{id}/ - Retrieve a specific author with their books

Permission Summary:
- Read operations (GET): Available to all users (authenticated and unauthenticated)
- Write operations (POST, PUT, PATCH, DELETE): Require authentication

The URL patterns follow RESTful conventions and provide clear, intuitive endpoints
for all CRUD operations on both Book and Author resources.
"""
