from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, UserUpdateForm


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_register_view_get(self):
        """Test registration page loads correctly"""
        response = self.client.get(reverse('blog:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_valid(self):
        """Test successful user registration"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('blog:register'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        """Test login page loads correctly"""
        response = self.client.get(reverse('blog:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_view_post_valid(self):
        """Test successful user login"""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = self.client.post(reverse('blog:login'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_login_view_post_invalid(self):
        """Test failed login with invalid credentials"""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('blog:login'), form_data)
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response, 'Please enter a correct username and password')

    def test_logout_view(self):
        """Test user logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that user is no longer authenticated after following redirect
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_profile_view_authenticated(self):
        """Test profile page for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('blog:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile Management')
        self.assertIsInstance(response.context['form'], UserUpdateForm)

    def test_profile_view_unauthenticated(self):
        """Test profile page redirects for unauthenticated user"""
        response = self.client.get(reverse('blog:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_update_post(self):
        """Test profile update functionality"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'first_name': 'Updated',
            'last_name': 'Name',
        }
        response = self.client.post(reverse('blog:profile'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Verify changes were saved
        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_custom_user_creation_form(self):
        """Test custom registration form validation"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form(self):
        """Test user update form validation"""
        form_data = {
            'username': 'testuser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        form = UserUpdateForm(data=form_data, instance=self.test_user)
        self.assertTrue(form.is_valid())
