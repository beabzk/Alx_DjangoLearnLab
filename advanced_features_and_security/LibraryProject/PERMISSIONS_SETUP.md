# Permissions and Groups Setup Documentation

## Overview
This document explains how permissions and groups are configured and used in the Django Library Management application.

## Custom Permissions
The following custom permissions have been defined for the Book model in `relationship_app/models.py`:

- `can_view`: Allows users to view books
- `can_create`: Allows users to create new books
- `can_edit`: Allows users to edit existing books
- `can_delete`: Allows users to delete books

## Groups Configuration
Three user groups have been created with different permission levels:

### 1. Viewers Group
- **Permissions**: `can_view`
- **Description**: Users in this group can only view books but cannot create, edit, or delete them.
- **Use Case**: Regular library members who need read-only access.

### 2. Editors Group
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Description**: Users in this group can view, create, and edit books but cannot delete them.
- **Use Case**: Library staff who manage the book catalog but don't have deletion privileges.

### 3. Admins Group
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Description**: Users in this group have full access to all book operations.
- **Use Case**: Library administrators with complete management privileges.

## Views with Permission Enforcement
The following views have been protected with permission decorators:

### `list_books` view
- **Required Permission**: `relationship_app.can_view`
- **Decorator**: `@permission_required('relationship_app.can_view', raise_exception=True)`
- **Description**: Users must have view permission to see the list of books.

### `add_book` view
- **Required Permission**: `relationship_app.can_create`
- **Decorator**: `@permission_required('relationship_app.can_create', raise_exception=True)`
- **Description**: Users must have create permission to add new books.

### `edit_book` view
- **Required Permission**: `relationship_app.can_edit`
- **Decorator**: `@permission_required('relationship_app.can_edit', raise_exception=True)`
- **Description**: Users must have edit permission to modify existing books.

### `delete_book` view
- **Required Permission**: `relationship_app.can_delete`
- **Decorator**: `@permission_required('relationship_app.can_delete', raise_exception=True)`
- **Description**: Users must have delete permission to remove books.

## Setup Instructions

### 1. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Set Up Groups and Permissions
```bash
python manage.py setup_groups
```

This command will:
- Create the three groups (Viewers, Editors, Admins)
- Assign appropriate permissions to each group
- Display a summary of the setup

### 3. Assign Users to Groups
Use the Django admin interface or Django shell to assign users to appropriate groups:

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Get a user and assign to a group
user = User.objects.get(username='example_user')
viewers_group = Group.objects.get(name='Viewers')
user.groups.add(viewers_group)
```

## Testing Permissions

### Manual Testing Approach
1. Create test users and assign them to different groups
2. Log in as these users and attempt to access various parts of the application
3. Verify that permissions are enforced correctly

### Expected Behavior
- **Viewers**: Can access book list but get permission denied on create/edit/delete operations
- **Editors**: Can view, create, and edit books but get permission denied on delete operations
- **Admins**: Can perform all operations without restrictions

## Error Handling
When users attempt to access views without proper permissions:
- The `raise_exception=True` parameter in permission decorators causes a `PermissionDenied` exception
- Django will display a 403 Forbidden page
- This provides clear feedback to users about access restrictions

## Security Notes
- All sensitive views are protected with appropriate permission checks
- The permission system follows the principle of least privilege
- Users only get the minimum permissions necessary for their role
- Permission checks are enforced at the view level to prevent unauthorized access
