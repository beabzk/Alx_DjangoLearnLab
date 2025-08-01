# LibraryProject

This is a Django-based web application for managing a library system. It is designed as a learning project to demonstrate the basics of Django, including advanced features like custom user models, permissions, and security best practices.

## Features

### Custom User Model
- Extended Django's default user model with additional fields:
  - `date_of_birth`: User's date of birth
  - `profile_photo`: User's profile photo

### Permissions and Groups System
The application implements a comprehensive permissions system with custom permissions and user groups.

#### Custom Permissions
The following custom permissions are defined for the Book model:
- `can_view`: Allows users to view books
- `can_create`: Allows users to create new books
- `can_edit`: Allows users to edit existing books
- `can_delete`: Allows users to delete books

#### User Groups
Three user groups have been created with different permission levels:

1. **Viewers Group**
   - Permissions: `can_view`
   - Description: Users can only view books but cannot create, edit, or delete them
   - Use Case: Regular library members with read-only access

2. **Editors Group**
   - Permissions: `can_view`, `can_create`, `can_edit`
   - Description: Users can view, create, and edit books but cannot delete them
   - Use Case: Library staff who manage the book catalog

3. **Admins Group**
   - Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
   - Description: Users have full access to all book operations
   - Use Case: Library administrators with complete management privileges

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django pillow
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Set Up Groups and Permissions
```bash
python manage.py setup_groups
```

### 5. Create Test Users (Optional)
```bash
python manage.py create_test_users
```

This will create test users for each group:
- `viewer_user` / `testpass123` (Viewers group)
- `editor_user` / `testpass123` (Editors group)
- `admin_user` / `testpass123` (Admins group)

### 6. Run the Development Server
```bash
python manage.py runserver
```

## Testing Permissions

1. Log in with different test users
2. Try accessing different book operations
3. Users without proper permissions will see 403 Forbidden errors
4. Verify that permissions are enforced correctly:
   - Viewers can only view books
   - Editors can view, create, and edit books
   - Admins can perform all operations

## Security Features

- Custom user model with additional fields
- Permission-based access control
- Group-based user management
- Secure view decorators with `@permission_required`
- Proper error handling for unauthorized access

## Project Structure

```
LibraryProject/
├── LibraryProject/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── bookshelf/
│   ├── models.py          # Custom User and Book models with permissions
│   ├── views.py           # Views with permission decorators
│   ├── admin.py           # Custom admin configuration
│   └── templates/
├── relationship_app/
│   ├── models.py          # Additional models with permissions
│   ├── views.py           # Views with permission enforcement
│   ├── management/
│   │   └── commands/
│   │       ├── setup_groups.py      # Command to set up groups
│   │       └── create_test_users.py # Command to create test users
│   └── templates/
└── README.md
```