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

## Next Steps

The following tasks will be implemented in subsequent phases:
- [ ] Task 1: Custom Views and Generic Views
- [ ] Task 2: Filtering, Searching, and Ordering
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
