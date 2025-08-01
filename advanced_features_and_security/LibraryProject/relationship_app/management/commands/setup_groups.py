from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book as RelationshipBook
from bookshelf.models import Book as BookshelfBook


class Command(BaseCommand):
    help = 'Create groups and assign permissions for the library system'

    def handle(self, *args, **options):
        """
        Set up user groups in Django and assign the newly created permissions to these groups.
        Creates groups like Editors, Viewers, and Admins with appropriate permissions.
        """

        # Get permissions for both Book models
        relationship_permissions = []
        bookshelf_permissions = []

        # Get the content type for the relationship_app Book model
        relationship_book_content_type = ContentType.objects.get_for_model(RelationshipBook)

        # Get the content type for the bookshelf Book model
        bookshelf_book_content_type = ContentType.objects.get_for_model(BookshelfBook)

        # Get or create the custom permissions for relationship_app
        for codename, name in [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=relationship_book_content_type,
            )
            relationship_permissions.append(perm)

        # Get or create the custom permissions for bookshelf
        for codename, name in [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=bookshelf_book_content_type,
            )
            bookshelf_permissions.append(perm)

        # Combine all permissions
        all_permissions = relationship_permissions + bookshelf_permissions
        
        # Create groups and assign permissions

        # Filter permissions by type
        view_permissions = [p for p in all_permissions if p.codename == 'can_view']
        create_permissions = [p for p in all_permissions if p.codename == 'can_create']
        edit_permissions = [p for p in all_permissions if p.codename == 'can_edit']
        delete_permissions = [p for p in all_permissions if p.codename == 'can_delete']

        # 1. Viewers Group - can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.set(view_permissions)
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Viewers" group')
            )
        else:
            self.stdout.write('Updated "Viewers" group permissions')

        # 2. Editors Group - can view, create, and edit books (but not delete)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.set(view_permissions + create_permissions + edit_permissions)
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created "Editors" group')
            )
        else:
            self.stdout.write('Updated "Editors" group permissions')

        # 3. Admins Group - can perform all operations
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.set(all_permissions)
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
