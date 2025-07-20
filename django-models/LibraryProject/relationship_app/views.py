from django.shortcuts import render
from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

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

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redirect to the login page on successful registration
    template_name = 'relationship_app/register.html'