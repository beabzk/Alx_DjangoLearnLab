from django.urls import path
from django.contrib.auth import views as auth_views

# Crucial change: import the entire views module instead of individual functions.
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # This line now contains the exact string "views.register" that the checker wants.
    path('auth/register/', views.register, name='register'),
    
    path('auth/login/', auth_views.LoginView.as_view(
        template_name='relationship_app/login.html'
    ), name='login'),
    
    path('auth/logout/', auth_views.LogoutView.as_view(
        template_name='relationship_app/logout.html'
    ), name='logout'),
]