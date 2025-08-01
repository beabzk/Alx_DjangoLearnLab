from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Import models
from .models import Book, Library, Author
# Import the form
from .forms import BookForm

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

# 1. Implement Function-based View:
@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    """
    This function-based view queries all books from the database
    and renders them in a simple list. Requires 'can_view' permission.
    """
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# 2. Implement Class-based View:
class LibraryDetailView(DetailView):
    """
    This class-based view displays details for a specific library,
    including a list of all books it contains. It uses Django's
    built-in DetailView.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' # This makes the variable 'library' available in the template


# 3. Implement User Registration:
def register(request):
    """
    Handles user registration. Creates a new user and then uses the imported
    'login' function to log them in automatically.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in automatically after registration
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Helper functions to check roles for the decorator
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-specific views
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """
    View to create a new book. Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})

@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    View to edit an existing book. Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit'})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    View to delete a book. Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})