from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.

    Provides a clean interface for managing authors in the Django admin,
    including search functionality and display customization.
    """
    list_display = ['name', 'book_count']
    search_fields = ['name']
    ordering = ['name']

    def book_count(self, obj):
        """Display the number of books by this author."""
        return obj.books.count()
    book_count.short_description = 'Number of Books'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.

    Provides comprehensive management interface for books including
    filtering, searching, and organized display of book information.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['title']
    autocomplete_fields = ['author']
