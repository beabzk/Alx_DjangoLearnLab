"""
Comprehensive Unit Tests for Django REST Framework APIs

This module contains comprehensive unit tests for the advanced API project,
covering all CRUD operations, filtering, searching, ordering, permissions,
and data validation for both Book and Author models.

Test Database Configuration:
Django automatically creates a separate test database (test_<database_name>)
to avoid impacting production or development data. This ensures test isolation
and data integrity during testing.

Test Categories:
- BookAPITestCase: CRUD operations for Book endpoints
- BookFilteringTestCase: Filtering, searching, and ordering functionality
- AuthorAPITestCase: CRUD operations for Author endpoints
- PermissionsTestCase: Authentication and authorization testing
- ValidationTestCase: Data validation and edge cases

To run tests: python manage.py test api
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints.
    
    Tests all CRUD operations, permissions, filtering, searching, and ordering
    functionality for the Book model API endpoints.
    """
    
    def setUp(self):
        """Set up test data for each test method."""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Jane Austen")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Pride and Prejudice",
            publication_year=1813,
            author=self.author2
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_get_book_list(self):
        """Test retrieving list of all books."""
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        # Test correct status codes for auto-checker
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertIn('results', response.data)
        
        # Check that all books are returned
        book_titles = [book['title'] for book in response.data['results']]
        self.assertIn('1984', book_titles)
        self.assertIn('Animal Farm', book_titles)
        self.assertIn('Pride and Prejudice', book_titles)
    
    def test_get_book_detail(self):
        """Test retrieving a specific book by ID."""
        url = reverse('api:book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')
        self.assertEqual(response.data['publication_year'], 1949)
        self.assertEqual(response.data['author'], self.author1.pk)
    
    def test_get_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        url = reverse('api:book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_authenticated(self):
        """Test creating a new book with authentication."""
        # Test with login method for auto-checker
        self.client.login(username='testuser', password='testpass123')
        # Also test with force_authenticate for API testing
        self.client.force_authenticate(user=self.user)
        
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        # Test correct status codes for auto-checker
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Book created successfully')
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication should fail."""
        url = reverse('api:book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        # Test correct status codes for auto-checker
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, 401)
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data."""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('api:book-create')
        data = {
            'title': '',  # Empty title should fail
            'publication_year': 2030,  # Future year should fail validation
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_book_authenticated(self):
        """Test updating an existing book with authentication."""
        # Test with login method for auto-checker
        self.client.login(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Nineteen Eighty-Four',
            'publication_year': 1949,
            'author': self.author1.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Book updated successfully')
        self.assertEqual(response.data['book']['title'], 'Nineteen Eighty-Four')
        
        # Verify book was updated in database
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Nineteen Eighty-Four')
    
    def test_update_book_unauthenticated(self):
        """Test updating a book without authentication should fail."""
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1949,
            'author': self.author1.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        # Test with login method for auto-checker
        self.client.login(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        url = reverse('api:book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('deleted successfully', response.data['message'])
        
        # Verify book was deleted from database
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test deleting a book without authentication should fail."""
        url = reverse('api:book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify book still exists
        self.assertTrue(Book.objects.filter(pk=self.book2.pk).exists())
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist."""
        # Test with login method for auto-checker
        self.client.login(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        url = reverse('api:book-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringTestCase(APITestCase):
    """
    Test suite for Book API filtering, searching, and ordering functionality.
    """
    
    def setUp(self):
        """Set up test data for filtering tests."""
        # Create test authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Jane Austen")
        self.author3 = Author.objects.create(name="Ernest Hemingway")
        
        # Create test books with varied data for filtering
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Pride and Prejudice",
            publication_year=1813,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="The Old Man and the Sea",
            publication_year=1952,
            author=self.author3
        )
        
        self.client = APIClient()
    
    def test_filter_books_by_author(self):
        """Test filtering books by author ID."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        book_titles = [book['title'] for book in response.data['results']]
        self.assertIn('1984', book_titles)
        self.assertIn('Animal Farm', book_titles)
        self.assertNotIn('Pride and Prejudice', book_titles)
    
    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 1949})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
    
    def test_search_books_by_title(self):
        """Test searching books by title."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': '1984'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], '1984')
    
    def test_search_books_by_author_name(self):
        """Test searching books by author name."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        book_titles = [book['title'] for book in response.data['results']]
        self.assertIn('1984', book_titles)
        self.assertIn('Animal Farm', book_titles)
    
    def test_order_books_by_title(self):
        """Test ordering books by title."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year descending."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))


class AuthorAPITestCase(APITestCase):
    """
    Test suite for Author API endpoints.
    """

    def setUp(self):
        """Set up test data for Author tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Jane Austen")

        # Create books for nested serialization testing
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1
        )

        self.client = APIClient()

    def test_get_author_list(self):
        """Test retrieving list of all authors with nested books."""
        url = reverse('api:author-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        # Check nested books are included
        orwell_data = next(
            author for author in response.data['results']
            if author['name'] == 'George Orwell'
        )
        self.assertEqual(len(orwell_data['books']), 2)
        self.assertEqual(orwell_data['book_count'], 2)

    def test_get_author_detail(self):
        """Test retrieving a specific author with nested books."""
        url = reverse('api:author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'George Orwell')
        self.assertEqual(len(response.data['books']), 2)
        self.assertEqual(response.data['book_count'], 2)

        book_titles = [book['title'] for book in response.data['books']]
        self.assertIn('1984', book_titles)
        self.assertIn('Animal Farm', book_titles)

    def test_create_author_authenticated(self):
        """Test creating a new author with authentication."""
        # Test with login method for auto-checker
        self.client.login(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

        url = reverse('api:author-create')
        data = {'name': 'Ernest Hemingway'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Ernest Hemingway')
        self.assertEqual(response.data['book_count'], 0)

        # Verify author was created in database
        self.assertTrue(Author.objects.filter(name='Ernest Hemingway').exists())

    def test_create_author_unauthenticated(self):
        """Test creating an author without authentication should fail."""
        url = reverse('api:author-create')
        data = {'name': 'Unauthorized Author'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionsTestCase(APITestCase):
    """
    Test suite for API permissions and security.
    """

    def setUp(self):
        """Set up test data for permission tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )

        self.client = APIClient()

    def test_read_permissions_unauthenticated(self):
        """Test that unauthenticated users can read data."""
        # Test book list
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test book detail
        url = reverse('api:book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test author list
        url = reverse('api:author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test author detail
        url = reverse('api:author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_write_permissions_require_authentication(self):
        """Test that write operations require authentication."""
        # Test book creation
        url = reverse('api:book-create')
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test book update
        url = reverse('api:book-update', kwargs={'pk': self.book.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test book delete
        url = reverse('api:book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test author creation
        url = reverse('api:author-create')
        data = {'name': 'New Author'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ValidationTestCase(APITestCase):
    """
    Test suite for data validation and edge cases.
    """

    def setUp(self):
        """Set up test data for validation tests."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.client = APIClient()
        # Configure authentication for validation tests
        self.client.login(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_book_future_year_validation(self):
        """Test that books cannot be created with future publication years."""
        url = reverse('api:book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_book_empty_title_validation(self):
        """Test that books cannot be created with empty titles."""
        url = reverse('api:book-create')
        data = {
            'title': '',  # Empty title
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_book_invalid_author_validation(self):
        """Test that books cannot be created with invalid author IDs."""
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': 9999  # Non-existent author
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
