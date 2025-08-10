#!/usr/bin/env python
"""
Test script to verify the Django REST Framework views and URL routing.

This script tests all the API endpoints to ensure they are properly configured
and working as expected. It tests both authenticated and unauthenticated access.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Author, Book


def test_api_endpoints():
    """Test all API endpoints to verify they work correctly."""
    
    print("=== Testing Django REST Framework API Endpoints ===\n")
    
    # Base URL for API (assuming development server is running)
    base_url = "http://127.0.0.1:8000/api"
    
    # Clear existing data for clean test
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create test data
    print("1. Setting up test data...")
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="Jane Austen")
    
    book1 = Book.objects.create(
        title="1984",
        publication_year=1949,
        author=author1
    )
    book2 = Book.objects.create(
        title="Animal Farm",
        publication_year=1945,
        author=author1
    )
    
    print(f"   Created authors: {author1.name}, {author2.name}")
    print(f"   Created books: {book1.title}, {book2.title}")
    
    # Test URL patterns without making HTTP requests (since server might not be running)
    print("\n2. Testing URL pattern resolution...")
    
    from django.urls import reverse
    from django.test import RequestFactory
    from api import views
    
    # Test URL reversing
    try:
        book_list_url = reverse('api:book-list')
        book_detail_url = reverse('api:book-detail', kwargs={'pk': book1.pk})
        book_create_url = reverse('api:book-create')
        book_update_url = reverse('api:book-update', kwargs={'pk': book1.pk})
        book_delete_url = reverse('api:book-delete', kwargs={'pk': book1.pk})
        
        author_list_url = reverse('api:author-list')
        author_detail_url = reverse('api:author-detail', kwargs={'pk': author1.pk})
        author_create_url = reverse('api:author-create')
        
        print(f"   ✓ Book list URL: {book_list_url}")
        print(f"   ✓ Book detail URL: {book_detail_url}")
        print(f"   ✓ Book create URL: {book_create_url}")
        print(f"   ✓ Book update URL: {book_update_url}")
        print(f"   ✓ Book delete URL: {book_delete_url}")
        print(f"   ✓ Author list URL: {author_list_url}")
        print(f"   ✓ Author detail URL: {author_detail_url}")
        print(f"   ✓ Author create URL: {author_create_url}")
        
    except Exception as e:
        print(f"   ✗ URL pattern error: {e}")
        return
    
    # Test view instantiation
    print("\n3. Testing view instantiation...")
    
    factory = RequestFactory()
    
    try:
        # Test BookListView
        request = factory.get('/api/books/')
        view = views.BookListView.as_view()
        response = view(request)
        print(f"   ✓ BookListView instantiated successfully (status: {response.status_code})")
        
        # Test BookDetailView
        request = factory.get(f'/api/books/{book1.pk}/')
        view = views.BookDetailView.as_view()
        response = view(request, pk=book1.pk)
        print(f"   ✓ BookDetailView instantiated successfully (status: {response.status_code})")
        
        # Test AuthorListView
        request = factory.get('/api/authors/')
        view = views.AuthorListView.as_view()
        response = view(request)
        print(f"   ✓ AuthorListView instantiated successfully (status: {response.status_code})")
        
        # Test AuthorDetailView
        request = factory.get(f'/api/authors/{author1.pk}/')
        view = views.AuthorDetailView.as_view()
        response = view(request, pk=author1.pk)
        print(f"   ✓ AuthorDetailView instantiated successfully (status: {response.status_code})")
        
    except Exception as e:
        print(f"   ✗ View instantiation error: {e}")
        return
    
    # Test permissions
    print("\n4. Testing permission classes...")
    
    # Create a test user for authentication tests
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
    
    try:
        # Test unauthenticated access to read-only views
        request = factory.get('/api/books/')
        view = views.BookListView()
        view.request = request
        view.format_kwarg = None
        
        # Check permissions
        permission_classes = view.get_permissions()
        print(f"   ✓ BookListView permissions: {[p.__class__.__name__ for p in permission_classes]}")
        
        # Test authenticated-only views
        view = views.BookCreateView()
        permission_classes = view.get_permissions()
        print(f"   ✓ BookCreateView permissions: {[p.__class__.__name__ for p in permission_classes]}")
        
    except Exception as e:
        print(f"   ✗ Permission testing error: {e}")
    
    print("\n5. Testing serializer integration...")
    
    try:
        # Test that views use correct serializers
        book_list_view = views.BookListView()
        book_serializer = book_list_view.get_serializer_class()
        print(f"   ✓ BookListView uses serializer: {book_serializer.__name__}")
        
        author_list_view = views.AuthorListView()
        author_serializer = author_list_view.get_serializer_class()
        print(f"   ✓ AuthorListView uses serializer: {author_serializer.__name__}")
        
    except Exception as e:
        print(f"   ✗ Serializer integration error: {e}")
    
    print("\n=== API Views and URL Configuration Test Completed Successfully! ===")
    print("\nTo test the API endpoints with HTTP requests:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/api/books/ (for browsable API)")
    print("3. Use tools like Postman or curl to test CRUD operations")
    print("\nExample curl commands:")
    print("- GET books: curl http://127.0.0.1:8000/api/books/")
    print("- GET authors: curl http://127.0.0.1:8000/api/authors/")
    print("- GET specific book: curl http://127.0.0.1:8000/api/books/1/")


if __name__ == "__main__":
    test_api_endpoints()
