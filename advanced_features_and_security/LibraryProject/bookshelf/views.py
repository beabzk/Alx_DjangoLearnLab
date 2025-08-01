from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

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
    View to list all books. Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

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
