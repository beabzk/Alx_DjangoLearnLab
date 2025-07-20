from django.shortcuts import render, redirect

from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login

# Import models one by one
from .models import Book
from .models import Library

# 1. Implement Function-based View:
def list_books(request):
    """
    This function-based view queries all books from the database
    and renders them in a simple list.
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