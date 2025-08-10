from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books.

    This view handles GET requests to retrieve a list of all books in the database.
    It uses the BookSerializer to format the response data and supports pagination
    if configured in the project settings.

    Permissions: Read-only access for all users (authenticated and unauthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow read access to everyone


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.

    This view handles GET requests to retrieve a specific book instance
    using its primary key (ID). Returns 404 if the book doesn't exist.

    Permissions: Read-only access for all users (authenticated and unauthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow read access to everyone


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new book.

    This view handles POST requests to create new book instances.
    It validates the incoming data using BookSerializer and saves
    the new book to the database if validation passes.

    Permissions: Restricted to authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        """
        Custom method to handle additional logic during book creation.

        This method is called after validation but before saving.
        Can be used to set additional fields or perform custom logic.
        """
        # Save the book instance
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Custom create method to provide enhanced response handling.

        Overrides the default create method to provide more detailed
        responses and better error handling for book creation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'book': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying an existing book.

    This view handles PUT and PATCH requests to update book instances.
    PUT replaces the entire resource, while PATCH allows partial updates.
    The view validates data using BookSerializer before saving changes.

    Permissions: Restricted to authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_update(self, serializer):
        """
        Custom method to handle additional logic during book updates.

        This method is called after validation but before saving.
        Can be used to log changes, send notifications, or perform custom logic.
        """
        # Save the updated book instance
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Custom update method to provide enhanced response handling.

        Overrides the default update method to provide more detailed
        responses and better error handling for book updates.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                'message': 'Book updated successfully',
                'book': serializer.data
            },
            status=status.HTTP_200_OK
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book.

    This view handles DELETE requests to remove book instances from the database.
    Returns 204 No Content on successful deletion, 404 if book doesn't exist.

    Permissions: Restricted to authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to provide enhanced response handling.

        Overrides the default destroy method to provide confirmation
        messages and better error handling for book deletion.
        """
        instance = self.get_object()
        book_title = instance.title
        book_author = instance.author.name

        # Perform the deletion
        self.perform_destroy(instance)

        return Response(
            {
                'message': f'Book "{book_title}" by {book_author} deleted successfully'
            },
            status=status.HTTP_200_OK
        )


# Additional Author views for complete API functionality
class AuthorListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all authors with their books.

    This view returns all authors along with their nested book information
    using the AuthorSerializer. Useful for getting complete author profiles
    including their bibliography.

    Permissions: Read-only access for all users
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single author with their books.

    This view returns a specific author along with all their books
    using the nested AuthorSerializer. Perfect for author profile pages.

    Permissions: Read-only access for all users
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding new authors.

    This view handles POST requests to create new author instances.
    Note: This only creates the author; books must be added separately
    through the Book endpoints.

    Permissions: Restricted to authenticated users only
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
