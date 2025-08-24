from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm


class PostCRUDTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user1
        )

    def test_post_list_view(self):
        """Test that post list view works for all users"""
        response = self.client.get(reverse('blog:post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'testuser1')

    def test_post_detail_view(self):
        """Test that post detail view works for all users"""
        response = self.client.get(reverse('blog:post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post content')

    def test_post_create_view_authenticated(self):
        """Test post creation for authenticated users"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('blog:post-create'))
        self.assertEqual(response.status_code, 200)
        
        # Test post creation
        form_data = {
            'title': 'New Test Post',
            'content': 'This is a new test post content.',
        }
        response = self.client.post(reverse('blog:post-create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    def test_post_create_view_unauthenticated(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get(reverse('blog:post-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_post_update_view_author(self):
        """Test that post author can update their post"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('blog:post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test post update
        form_data = {
            'title': 'Updated Test Post',
            'content': 'This is updated content.',
        }
        response = self.client.post(reverse('blog:post-update', kwargs={'pk': self.post.pk}), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        updated_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.title, 'Updated Test Post')

    def test_post_update_view_non_author(self):
        """Test that non-authors cannot update posts"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('blog:post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_post_delete_view_author(self):
        """Test that post author can delete their post"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('blog:post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        
        # Test post deletion
        response = self.client.post(reverse('blog:post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_view_non_author(self):
        """Test that non-authors cannot delete posts"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('blog:post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_post_form_validation(self):
        """Test PostForm validation"""
        # Test valid form
        form_data = {
            'title': 'Valid Title',
            'content': 'Valid content for the post.',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test invalid form (empty title)
        form_data = {
            'title': '',
            'content': 'Valid content for the post.',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_author_assignment(self):
        """Test that post author is automatically set during creation"""
        self.client.login(username='testuser2', password='testpass123')
        form_data = {
            'title': 'Author Test Post',
            'content': 'Testing author assignment.',
        }
        response = self.client.post(reverse('blog:post-create'), form_data)
        self.assertEqual(response.status_code, 302)
        
        post = Post.objects.get(title='Author Test Post')
        self.assertEqual(post.author, self.user2)

    def test_post_permissions_loginrequiredmixin(self):
        """Test LoginRequiredMixin for post creation, update, and delete"""
        # Test create
        response = self.client.get(reverse('blog:post-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test update
        response = self.client.get(reverse('blog:post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test delete
        response = self.client.get(reverse('blog:post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_post_absolute_url(self):
        """Test Post model get_absolute_url method"""
        url = self.post.get_absolute_url()
        expected_url = reverse('blog:post-detail', kwargs={'pk': self.post.pk})
        self.assertEqual(url, expected_url)
