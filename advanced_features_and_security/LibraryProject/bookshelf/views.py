from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape
from .models import Book
from .forms import ExampleForm

"""
PERMISSIONS AND GROUPS SETUP:

Custom Permissions defined in Book model:
- can_view: Allows viewing books
- can_create: Allows creating new books
- can_edit: Allows editing existing books
- can_delete: Allows deleting books

Groups and their permissions:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

To set up groups and permissions, run:
python manage.py setup_groups

To create test users, run:
python manage.py create_test_users
"""

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure view to list all books with search functionality.
    Requires 'can_view' permission and implements security best practices.
    """
    # Use the secure search functionality
    return secure_book_search(request)

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book. Requires 'can_create' permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')

        if title and author and publication_year:
            Book.objects.create(
                title=title,
                author=author,
                publication_year=int(publication_year)
            )
            return redirect('book_list')

    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book. Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = int(request.POST.get('publication_year', book.publication_year))
        book.save()
        return redirect('book_list')

    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book. Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@csrf_protect
def form_example_view(request):
    """
    Secure form handling view demonstrating security best practices:
    - CSRF protection with @csrf_protect decorator
    - Input validation and sanitization through ExampleForm
    - XSS prevention through proper form handling
    - Safe error handling and user feedback
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the validated and sanitized data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            age = form.cleaned_data.get('age')

            # In a real application, you would save this data securely
            # For demonstration, we'll just show a success message
            messages.success(
                request,
                f'Thank you, {escape(name)}! Your form has been submitted successfully.'
            )

            # Redirect after successful POST to prevent duplicate submissions
            return redirect('form_example')
        else:
            # Form has validation errors - they will be displayed in the template
            messages.error(
                request,
                'Please correct the errors below and try again.'
            )
    else:
        # GET request - show empty form
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_view', raise_exception=True)
def secure_book_search(request):
    """
    Secure search view demonstrating protection against SQL injection:
    - Uses Django ORM with parameterized queries
    - Validates and sanitizes search input
    - Implements pagination for performance
    - Escapes output to prevent XSS
    """
    books = Book.objects.all()
    search_query = None

    if request.GET.get('search'):
        search_query = request.GET.get('search').strip()

        # Validate search query length to prevent abuse
        if len(search_query) > 100:
            messages.error(request, 'Search query is too long.')
            return redirect('book_list')

        # Escape the search query to prevent XSS
        search_query = escape(search_query)

        # Use Django ORM with Q objects for safe querying (prevents SQL injection)
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # Implement pagination for better performance and user experience
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }

    return render(request, 'bookshelf/book_list.html', context)
