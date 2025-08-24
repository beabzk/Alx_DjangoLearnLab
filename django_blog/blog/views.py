from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm

# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-published_date')[:5]  # Get latest 5 posts
    return render(request, 'blog/home.html', {'posts': posts})


# Custom Registration View
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('blog:login')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'Account created for {user.username}! You can now log in.')
        return super().form_valid(form)


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blog:home')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


# Custom Logout View
class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been logged out successfully!')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Handle GET request for logout"""
        return self.post(request, *args, **kwargs)


# Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})
