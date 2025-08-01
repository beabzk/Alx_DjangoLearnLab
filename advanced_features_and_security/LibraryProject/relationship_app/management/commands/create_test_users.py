from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups for testing permissions'

    def handle(self, *args, **options):
        """
        Create test users and assign them to different groups.
        This allows manual testing of the permission system.
        """
        User = get_user_model()
        
        # Get the groups
        try:
            viewers_group = Group.objects.get(name='Viewers')
            editors_group = Group.objects.get(name='Editors')
            admins_group = Group.objects.get(name='Admins')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Groups not found. Please run "python manage.py setup_groups" first.')
            )
            return
        
        # Create test users
        test_users = [
            {
                'username': 'viewer_user',
                'email': 'viewer@example.com',
                'password': 'testpass123',
                'group': viewers_group,
                'description': 'Test user with view-only permissions'
            },
            {
                'username': 'editor_user',
                'email': 'editor@example.com',
                'password': 'testpass123',
                'group': editors_group,
                'description': 'Test user with create and edit permissions'
            },
            {
                'username': 'admin_user',
                'email': 'admin@example.com',
                'password': 'testpass123',
                'group': admins_group,
                'description': 'Test user with full permissions'
            }
        ]
        
        for user_data in test_users:
            # Create user if it doesn't exist
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user_data["username"]}')
                )
            else:
                self.stdout.write(f'User {user_data["username"]} already exists')
            
            # Add user to group
            user.groups.clear()  # Remove from all groups first
            user.groups.add(user_data['group'])
            
            self.stdout.write(
                f'  - Assigned to group: {user_data["group"].name}'
            )
            self.stdout.write(
                f'  - Description: {user_data["description"]}'
            )
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS('Test users created successfully!')
        )
        
        # Display testing instructions
        self.stdout.write('\n--- Testing Instructions ---')
        self.stdout.write('1. Start the development server: python manage.py runserver')
        self.stdout.write('2. Log in with different test users:')
        self.stdout.write('   - viewer_user / testpass123 (can only view)')
        self.stdout.write('   - editor_user / testpass123 (can view, create, edit)')
        self.stdout.write('   - admin_user / testpass123 (can do everything)')
        self.stdout.write('3. Try accessing different book operations to test permissions')
        self.stdout.write('4. Users without proper permissions should see 403 Forbidden errors')
