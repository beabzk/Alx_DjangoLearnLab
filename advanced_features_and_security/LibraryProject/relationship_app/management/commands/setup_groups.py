from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book


class Command(BaseCommand):
    help = 'Create groups and assign permissions for the library system'

    def handle(self, *args, **options):
        """
        Set up user groups in Django and assign the newly created permissions to these groups.
        Creates groups like Editors, Viewers, and Admins with appropriate permissions.
        """
        
        # Get the content type for the Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create the custom permissions
        can_view, created = Permission.objects.get_or_create(
            codename='can_view',
            name='Can view book',
            content_type=book_content_type,
        )
        
        can_create, created = Permission.objects.get_or_create(
            codename='can_create',
            name='Can create book',
            content_type=book_content_type,
        )
        
        can_edit, created = Permission.objects.get_or_create(
            codename='can_edit',
            name='Can edit book',
            content_type=book_content_type,
        )
        
        can_delete, created = Permission.objects.get_or_create(
            codename='can_delete',
            name='Can delete book',
            content_type=book_content_type,
        )
        
        # Create groups and assign permissions
        
        # 1. Viewers Group - can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.set([can_view])
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Viewers" group')
            )
        else:
            self.stdout.write('Updated "Viewers" group permissions')
        
        # 2. Editors Group - can view, create, and edit books (but not delete)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.set([can_view, can_create, can_edit])
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Editors" group')
            )
        else:
            self.stdout.write('Updated "Editors" group permissions')
        
        # 3. Admins Group - can perform all operations
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.set([can_view, can_create, can_edit, can_delete])
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Admins" group')
            )
        else:
            self.stdout.write('Updated "Admins" group permissions')
        
        self.stdout.write(
            self.style.SUCCESS('Groups and permissions setup completed successfully!')
        )
        
        # Display summary
        self.stdout.write('\n--- Groups and Permissions Summary ---')
        self.stdout.write(f'Viewers: {[p.codename for p in viewers_group.permissions.all()]}')
        self.stdout.write(f'Editors: {[p.codename for p in editors_group.permissions.all()]}')
        self.stdout.write(f'Admins: {[p.codename for p in admins_group.permissions.all()]}')
