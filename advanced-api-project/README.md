# Advanced API Development with Django REST Framework

This project demonstrates advanced API development concepts using Django REST Framework, including custom serializers, generic views, filtering, searching, ordering, and comprehensive testing.

## Project Overview

The project implements a library management API with the following core models:
- **Author**: Represents book authors
- **Book**: Represents individual books with relationships to authors

## Features Implemented

### Task 0: Custom Serializers ✅
- Django project setup with Django REST Framework
- Custom Author and Book models with proper relationships
- Advanced serializers with nested relationships and validation
- Custom validation for publication year (prevents future dates)

### Task 1: Custom Views and Generic Views ✅
- Complete CRUD operations using DRF generic views
- Proper URL routing with RESTful endpoints
- Permission-based access control (authenticated vs unauthenticated)
- Enhanced response handling with custom messages
- Comprehensive API documentation and testing

### Task 2: Filtering, Searching, and Ordering ✅
- Advanced filtering capabilities with custom filter classes
- Full-text search across multiple fields
- Flexible ordering by any field
- Range filters and case-insensitive searches
- Integration with DRF filter backends

## Project Structure

```
advanced-api-project/
├── advanced_api_project/          # Main project directory
│   ├── settings.py               # Project settings with DRF configuration
│   ├── urls.py                   # Main URL configuration
│   └── ...
├── api/                          # Main API application
│   ├── models.py                 # Author and Book models
│   ├── serializers.py            # Custom serializers with validation
│   ├── views.py                  # API views with filtering/searching/ordering
│   ├── filters.py                # Custom filter classes for advanced querying
│   ├── admin.py                  # Django admin configuration
│   ├── migrations/               # Database migrations
│   └── ...
├── test_setup.py                 # Test script for models and serializers
├── manage.py                     # Django management script
└── README.md                     # This file
```

## Models

### Author Model
- **name**: CharField(max_length=100) - Author's full name
- **Relationships**: One-to-many with Book (one author can have many books)
- **Meta options**: Ordered by name, string representation shows author name

### Book Model
- **title**: CharField(max_length=200) - Book title
- **publication_year**: IntegerField - Year of publication
- **author**: ForeignKey to Author with CASCADE delete and 'books' related_name
- **Meta options**: Ordered by title, unique constraint on (title, author)

## Serializers

### BookSerializer
- Serializes all Book model fields
- **Custom validation**: Ensures publication_year is not in the future
- Provides detailed error messages for validation failures

### AuthorSerializer
- Includes author name and nested book serialization
- **Nested relationships**: Uses BookSerializer to include all author's books
- **Enhanced representation**: Adds book_count field for convenience
- Demonstrates efficient data retrieval with related objects

## Key Implementation Details

### Model Relationships
The relationship between Author and Book is implemented as a one-to-many foreign key:
```python
# In Book model
author = models.ForeignKey(
    Author, 
    on_delete=models.CASCADE, 
    related_name='books'
)
```

This allows:
- Each book to belong to exactly one author
- Each author to have multiple books
- Efficient reverse lookups using `author.books.all()`
- Automatic deletion of books when author is deleted

### Custom Validation
The BookSerializer includes custom validation to prevent future publication dates:
```python
def validate_publication_year(self, value):
    current_year = datetime.now().year
    if value > current_year:
        raise serializers.ValidationError(
            f"Publication year cannot be in the future. Current year is {current_year}."
        )
    return value
```

### Nested Serialization
The AuthorSerializer demonstrates nested serialization by including all related books:
```python
books = BookSerializer(many=True, read_only=True)
```

This provides complete author information including their bibliography in a single API call.

## API Endpoints

### Book Endpoints
- **GET /api/books/** - List all books (paginated)
  - Permission: Public access
  - Returns: Paginated list of books with basic information

- **POST /api/books/create/** - Create a new book
  - Permission: Authenticated users only
  - Body: `{"title": "Book Title", "publication_year": 2023, "author": 1}`
  - Returns: Created book data with success message

- **GET /api/books/{id}/** - Retrieve specific book
  - Permission: Public access
  - Returns: Single book details

- **PUT/PATCH /api/books/update/{id}/** - Update existing book
  - Permission: Authenticated users only
  - Body: Full (PUT) or partial (PATCH) book data
  - Returns: Updated book data with success message

- **DELETE /api/books/delete/{id}/** - Delete book
  - Permission: Authenticated users only
  - Returns: Deletion confirmation message

### Author Endpoints
- **GET /api/authors/** - List all authors with their books
  - Permission: Public access
  - Returns: Authors with nested book information and book count

- **POST /api/authors/create/** - Create a new author
  - Permission: Authenticated users only
  - Body: `{"name": "Author Name"}`
  - Returns: Created author data

- **GET /api/authors/{id}/** - Retrieve specific author with books
  - Permission: Public access
  - Returns: Author details with all their books

## Advanced Query Features

### Filtering
Both Book and Author endpoints support advanced filtering:

#### Book Filtering
- **Basic filters**: `?title=1984`, `?author=1`, `?publication_year=1949`
- **Case-insensitive title search**: `?title_icontains=animal`
- **Author name filtering**: `?author_name=orwell`
- **Year range filters**:
  - `?publication_year_gte=1940` (books from 1940 onwards)
  - `?publication_year_lte=1950` (books up to 1950)
  - `?publication_year_range=1940,1950` (books between 1940-1950)

#### Author Filtering
- **Name filtering**: `?name=George Orwell`
- **Case-insensitive name search**: `?name_icontains=george`
- **Authors with/without books**: `?has_books=true` or `?has_books=false`

### Searching
Full-text search across multiple fields:
- **Books**: `?search=orwell` (searches in title and author name)
- **Authors**: `?search=george` (searches in author name)

### Ordering
Sort results by any field:
- **Books**:
  - `?ordering=title` (A-Z)
  - `?ordering=-publication_year` (newest first)
  - `?ordering=author__name` (by author name)
- **Authors**:
  - `?ordering=name` (A-Z)
  - `?ordering=-name` (Z-A)

### Combined Queries
Combine multiple query parameters:
```
/api/books/?search=1984&publication_year_gte=1940&ordering=-publication_year
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Test the Setup
```bash
python test_setup.py
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## Testing

The project includes a comprehensive test script (`test_setup.py`) that verifies:
- Model creation and relationships
- Serializer functionality
- Custom validation logic
- Nested serialization
- Data integrity

Run the test with: `python test_setup.py`

### API Views Testing
The project includes comprehensive view testing (`test_views.py`) that verifies:
- URL pattern resolution and routing
- View instantiation and functionality
- Permission class configuration
- Serializer integration
- HTTP response handling

Run the view tests with: `python test_views.py`

## Django REST Framework Configuration

The project is configured with the following DRF settings:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

### Key Features:
- **Authentication**: Session and Basic authentication support
- **Permissions**: Read access for all, write access for authenticated users
- **Pagination**: 20 items per page with next/previous links
- **Browsable API**: Interactive web interface for testing endpoints

## Next Steps

The following tasks will be implemented in subsequent phases:
- [x] Task 1: Custom Views and Generic Views
- [x] Task 2: Filtering, Searching, and Ordering
- [ ] Task 3: Unit Tests for API endpoints

## Database Configuration

The project uses SQLite for development (configured in settings.py). The database file `db.sqlite3` is created automatically when running migrations.

## Admin Interface

Django admin is configured for both models with:
- Search functionality
- Filtering options
- Custom display fields
- Autocomplete for foreign key relationships

Access admin at: `http://localhost:8000/admin/` (after creating superuser)
