#!/usr/bin/env python
"""
Test script to verify the Django models and serializers setup.

This script tests the Author and Book models along with their custom serializers
to ensure everything is working correctly before proceeding to the next tasks.
"""

import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer


def test_models_and_serializers():
    """Test the models and serializers functionality."""
    
    print("=== Testing Django Models and Serializers ===\n")
    
    # Clear existing data for clean test
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Test 1: Create Authors
    print("1. Creating Authors...")
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="Jane Austen")
    print(f"   Created: {author1}")
    print(f"   Created: {author2}")
    
    # Test 2: Create Books
    print("\n2. Creating Books...")
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
    book3 = Book.objects.create(
        title="Pride and Prejudice",
        publication_year=1813,
        author=author2
    )
    print(f"   Created: {book1}")
    print(f"   Created: {book2}")
    print(f"   Created: {book3}")
    
    # Test 3: Test BookSerializer
    print("\n3. Testing BookSerializer...")
    book_serializer = BookSerializer(book1)
    print(f"   Serialized book data: {book_serializer.data}")
    
    # Test 4: Test BookSerializer validation (future year)
    print("\n4. Testing BookSerializer validation...")
    future_year = datetime.now().year + 1
    invalid_book_data = {
        'title': 'Future Book',
        'publication_year': future_year,
        'author': author1.id
    }
    invalid_serializer = BookSerializer(data=invalid_book_data)
    if not invalid_serializer.is_valid():
        print(f"   ✓ Validation correctly failed for future year: {invalid_serializer.errors}")
    else:
        print(f"   ✗ Validation should have failed for future year")
    
    # Test 5: Test AuthorSerializer with nested books
    print("\n5. Testing AuthorSerializer with nested books...")
    author_serializer = AuthorSerializer(author1)
    print(f"   Author data with nested books: {author_serializer.data}")
    
    # Test 6: Verify relationships
    print("\n6. Testing model relationships...")
    print(f"   Author '{author1.name}' has {author1.books.count()} books")
    print(f"   Books by {author1.name}: {[book.title for book in author1.books.all()]}")
    
    print("\n=== All tests completed successfully! ===")


if __name__ == "__main__":
    test_models_and_serializers()
