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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.client.force_authenticate(user=self.user)

        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_filter_books_by_year_range(self):
        """Test filtering books by publication year range."""
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year_gte': 1945})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # 1945, 1949, 1952

        # Test upper bound
        response = self.client.get(url, {'publication_year_lte': 1949})
        self.assertEqual(response.data['count'], 3)  # 1813, 1945, 1949
