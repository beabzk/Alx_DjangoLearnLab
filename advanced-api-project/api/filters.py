import django_filters
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Custom filter class for the Book model.
    
    This filter provides advanced filtering capabilities beyond simple field matching,
    including range filters, case-insensitive searches, and custom filter methods.
    
    Available filters:
    - title: Exact match or case-insensitive contains
    - title_icontains: Case-insensitive partial match for title
    - author: Filter by author ID
    - author_name: Case-insensitive partial match for author name
    - publication_year: Exact year match
    - publication_year_gte: Books published in or after this year
    - publication_year_lte: Books published in or before this year
    - publication_year_range: Books published between two years (comma-separated)
    """
    
    # Case-insensitive title search
    title_icontains = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text='Case-insensitive partial match for book title'
    )
    
    # Author name filtering (through foreign key relationship)
    author_name = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains',
        help_text='Case-insensitive partial match for author name'
    )
    
    # Publication year range filters
    publication_year_gte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text='Books published in or after this year'
    )
    
    publication_year_lte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text='Books published in or before this year'
    )
    
    # Range filter for publication year
    publication_year_range = django_filters.RangeFilter(
        field_name='publication_year',
        help_text='Books published between two years (format: min,max)'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author': ['exact'],
            'publication_year': ['exact', 'gte', 'lte'],
        }


class AuthorFilter(django_filters.FilterSet):
    """
    Custom filter class for the Author model.
    
    This filter provides advanced filtering capabilities for authors,
    including case-insensitive name searches and filtering by book count.
    
    Available filters:
    - name: Exact match or case-insensitive contains
    - name_icontains: Case-insensitive partial match for author name
    - has_books: Filter authors who have or don't have books
    """
    
    # Case-insensitive name search
    name_icontains = django_filters.CharFilter(
        field_name='name', 
        lookup_expr='icontains',
        help_text='Case-insensitive partial match for author name'
    )
    
    # Filter authors who have books
    has_books = django_filters.BooleanFilter(
        method='filter_has_books',
        help_text='Filter authors who have books (true) or no books (false)'
    )
    
    def filter_has_books(self, queryset, name, value):
        """
        Custom filter method to filter authors based on whether they have books.
        
        Args:
            queryset: The initial queryset
            name: The filter field name
            value: Boolean value (True for authors with books, False for authors without)
            
        Returns:
            Filtered queryset
        """
        if value is True:
            return queryset.filter(books__isnull=False).distinct()
        elif value is False:
            return queryset.filter(books__isnull=True)
        return queryset
    
    class Meta:
        model = Author
        fields = {
            'name': ['exact', 'icontains'],
        }
